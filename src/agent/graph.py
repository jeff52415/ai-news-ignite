import json
import operator
from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from agent.agents import AgentFactory
from utils import prompt_loader
from data_model.news import (
    AREA_LABELS,
    EVIDENCE_LABELS,
    CoverageReport,
    NewsArticle,
    NewsArticleList,
)
from data_model.selection import select_findings
from config.config import Config

# --- State Definition ---

class NewsGraphState(BaseModel):
    input_message: str
    news: NewsArticleList | None = Field(default=None, description="List of news articles")
    article: NewsArticle | None = Field(default=None, description="Single news article for processing")
    already_covered: list[str] = Field(
        default_factory=list,
        description="Titles already published, so later passes do not repeat them",
    )
    results: Annotated[list, operator.add] = Field(default_factory=list, description="Results accumulator")
    finished: bool = Field(default=False, description="Whether the graph has finished")

# --- Callback and Agent Factory ---

config = Config.load()
langfuse_handler = config.env.get_langfuse_handler()
agent_factory = AgentFactory()

def _articles_json(articles: list[NewsArticle]) -> str:
    payload = [article.model_dump(mode="json") for article in articles]
    return json.dumps(payload, indent=2)


def _as_article(article: NewsArticle | dict) -> NewsArticle:
    if isinstance(article, NewsArticle):
        return article
    return NewsArticle.model_validate(article)

# --- Node Definitions ---

async def search_news(state: NewsGraphState):
    """Fetch candidate developments that match the briefing criteria."""
    agent = await agent_factory.get_initial_search_agent()
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": state.input_message}]},
    )
    return {"news": response["structured_response"]}

async def filter_news(state: NewsGraphState):
    """Drop candidates the repository already covers. Keep the surviving dossiers intact."""
    if state.news is None or not state.news.articles:
        return {"news": NewsArticleList(articles=[]), "already_covered": []}

    assistant = await agent_factory.get_github_assistant(
        specific_tool=["get_file_contents", "get_me"],
        response_format=CoverageReport,
    )
    prompt = prompt_loader.get_prompt("news_filter")
    rendered_prompt = await prompt.template.render_async(
        news=_articles_json(state.news.articles)
    )
    response = await assistant.ainvoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
    )
    report: CoverageReport = response["structured_response"]
    covered_urls = {match.url.rstrip("/") for match in report.already_covered}
    covered_titles = {match.title.strip().lower() for match in report.already_covered}
    kept = [
        article
        for article in state.news.articles
        if article.url.rstrip("/") not in covered_urls
        and article.title.strip().lower() not in covered_titles
    ]
    covered_lines = [
        f"{match.title} | {match.url} | {match.reason}"
        for match in report.already_covered
    ]
    return {
        "news": NewsArticleList(articles=kept),
        "already_covered": covered_lines,
    }

async def verify_and_rank(state: NewsGraphState):
    """Re-check candidates against primary sources, then apply the code gate."""
    agent = await agent_factory.get_initial_search_agent(prompt_key="quality_gate")
    covered = "\n".join(state.already_covered) if state.already_covered else "(none)"
    candidates = _articles_json(state.news.articles) if state.news else "[]"
    prompt = prompt_loader.get_prompt("quality_gate_input")
    rendered_prompt = await prompt.template.render_async(
        today=date.today().isoformat(),
        already_covered=covered,
        candidates=candidates,
    )
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
    )
    verified = response["structured_response"]
    # The editor sometimes returns a prose review and an empty structured list.
    # The code gate still decides. An empty edit must not wipe candidates that pass it.
    incoming = state.news.articles if state.news else []
    pool = verified.articles or incoming
    selected = select_findings(
        pool,
        primary_window_days=config.app.primary_window_days,
        fallback_window_days=config.app.fallback_window_days,
        min_findings=config.app.min_findings,
        max_findings=config.app.max_findings,
    )
    return {"news": NewsArticleList(articles=selected)}

def route_articles(state: NewsGraphState):
    """Fan out one briefing section per surviving item."""
    articles = state.news.articles if state.news else []
    if not articles:
        return "collect_results"
    return [
        Send("summarize_and_publish", {"article": article})
        for article in articles
    ]

async def summarize_and_publish(state: NewsGraphState):
    """Summarize and publish a single article."""
    supervisor = await agent_factory.get_supervisor()
    prompt = prompt_loader.get_prompt("supervisor_agent_input")
    raw_article = state["article"] if isinstance(state, dict) else state.article
    article = _as_article(raw_article)
    rendered_prompt = await prompt.template.render_async(
        rank=article.rank,
        title=article.title,
        area_label=AREA_LABELS[article.area.value],
        source=article.source,
        date=article.date.isoformat(),
        url=article.url,
        availability=article.availability or "public",
        summary=article.summary,
        what_changed=article.what_changed,
        why_it_matters=article.why_it_matters,
        evidence_label=EVIDENCE_LABELS[article.evidence_kind.value],
        independently_validated="yes" if article.independently_validated else "no",
        evidence=article.evidence,
        novelty=article.novelty.value,
        practical_significance=article.practical_significance.value,
        confidence=article.confidence.value,
        links=article.links,
        github_stars=(
            article.github_stars
            if article.github_stars is not None
            else "not verified — omit the Stars line"
        ),
        github_recent_growth=(
            article.github_recent_growth or "not verified — omit the Recent growth line"
        ),
        technical_ideas=article.technical_ideas,
    )
    response = await supervisor.ainvoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
    )
    return {"results": [response["messages"][-1].content]}

async def collect_results(state: NewsGraphState):
    """Collects results from all summarized articles."""
    return {"finished": True}

def build_news_graph(debug: bool = False):
    # reference: https://langchain-ai.github.io/langgraph/how-tos/graph-api/#map-reduce-and-the-send-api
    builder = StateGraph(NewsGraphState)
    builder.add_node("search_news", search_news)
    builder.add_node("filter_news", filter_news)
    builder.add_node("verify_and_rank", verify_and_rank)
    builder.add_node("summarize_and_publish", summarize_and_publish)
    builder.add_node("collect_results", collect_results)

    builder.add_edge(START, "search_news")
    builder.add_edge("search_news", "filter_news")
    builder.add_edge("filter_news", "verify_and_rank")
    builder.add_conditional_edges(
        "verify_and_rank",
        route_articles,
        ["summarize_and_publish", "collect_results"],
    )
    builder.add_edge("summarize_and_publish", "collect_results")
    builder.add_edge("collect_results", END)

    return builder.compile(debug=debug)

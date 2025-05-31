import operator
from typing import Annotated
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langfuse.callback import CallbackHandler
from agent.agents import AgentFactory
from utils import prompt_loader
from data_model.news import NewsArticleList, NewsArticle

# --- State Definition ---

class NewsGraphState(BaseModel):
    input_message: str 
    news: NewsArticleList | None = Field(default=None, description="List of news articles")
    article: NewsArticle | None = Field(default=None, description="Single news article for processing")
    results: Annotated[list, operator.add] = Field(default_factory=list, description="Results accumulator")
    finished: bool = Field(default=False, description="Whether the graph has finished")

# --- Callback and Agent Factory ---

langfuse_handler = CallbackHandler()
agent_factory = AgentFactory()

# --- Node Definitions ---

async def search_news(state: NewsGraphState):
    """Fetch latest AI/ML news articles."""
    agent = await agent_factory.get_initial_search_agent()
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": state.input_message}]},
    )
    return {"news": response["structured_response"]}

async def filter_news(state: NewsGraphState):
    """Filter news articles using a custom prompt."""
    assistant = await agent_factory.get_github_assistant(
        specific_tool=["get_file_contents", "get_me"],
        response_format=NewsArticleList
    )
    prompt = prompt_loader.get_prompt("news_filter")
    rendered_prompt = await prompt.template.render_async(news=state.news.articles)
    response = await assistant.ainvoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
    )
    return {"news": response["structured_response"]}

async def map_to_articles(state: NewsGraphState):
    """Map each article to the summarization node using Send API."""
    return [Send("summarize_and_publish", {"article": article}) for article in state.news.articles]

# Modify summarize_and_publish to return the result for a single article
async def summarize_and_publish(state: NewsGraphState):
    """Summarize and publish a single article."""
    supervisor = await agent_factory.get_supervisor()
    prompt = prompt_loader.get_prompt("supervisor_agent_input")
    article = state["article"] # This is the article from the Send API
    rendered_prompt = await prompt.template.render_async(
        title=article.title,
        source=article.source,
        date=article.date,
        summary=article.summary,
        url_ref=article.url
    )
    response = await supervisor.ainvoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
    )
    # CORRECTED: Returns a list under the 'results' key for accumulation
    return {"results": [response["messages"][-1].content]}

# Add a reduction node
async def collect_results(state: NewsGraphState):
    """Collects results from all summarized articles."""
    # The 'results' field in NewsGraphState already handles accumulation
    # due to Annotated[list, operator.add]. So this node might just be a pass-through
    # or could perform additional aggregation if needed.
    return {"finished": True} # The accumulator already has them

def build_news_graph():
    # reference: https://langchain-ai.github.io/langgraph/how-tos/graph-api/#map-reduce-and-the-send-api
    builder = StateGraph(NewsGraphState)
    builder.add_node("search_news", search_news)
    builder.add_node("filter_news", filter_news)
    builder.add_node("map_to_articles", map_to_articles) # This node now acts as the dispatcher
    builder.add_node("summarize_and_publish", summarize_and_publish)
    builder.add_node("collect_results", collect_results)

    builder.add_edge(START, "search_news")
    builder.add_edge("search_news", "filter_news")

    # It returns a list of Send objects, and the targets are 'summarize_and_publish'
    builder.add_conditional_edges(
        "filter_news",          # The node from which to transition
        map_to_articles,        # The function that decides the next step(s)
        ["summarize_and_publish"] # The possible nodes that Send can target
    )


    builder.add_edge("summarize_and_publish", "collect_results")
    builder.add_edge("collect_results", END)



    return builder.compile()

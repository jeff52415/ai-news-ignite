"""Rank briefing candidates by technical significance, not popularity."""

from datetime import date, timedelta
from urllib.parse import urlparse

from data_model.news import EvidenceKind, Level, NewsArticle, Novelty, TechnicalArea, host_of

# One site can contribute several posts in a week. Keep the list from collapsing onto it.
MAX_PER_PROJECT = 2

NOVELTY_WEIGHT = {
    Novelty.fundamental: 5,
    Novelty.meaningful: 3,
    Novelty.incremental: 0,
}
LEVEL_WEIGHT = {Level.high: 3, Level.medium: 2, Level.low: 0}
EVIDENCE_WEIGHT = {
    EvidenceKind.independent_reproduction: 4,
    EvidenceKind.community_adoption: 3,
    EvidenceKind.credible_benchmark: 3,
    EvidenceKind.substantial_open_source: 3,
    EvidenceKind.primary_release: 2,
    EvidenceKind.technical_explanation: 2,
    EvidenceKind.developer_reported: 1,
}


def project_key(article: NewsArticle) -> str:
    """Group pages from one site. GitHub and Hugging Face group by owner."""
    host = host_of(article.url)
    parts = [part for part in urlparse(article.url).path.split("/") if part]
    if host == "github.com" and parts:
        return f"github.com/{parts[0].lower()}"
    if host in {"huggingface.co", "hf.co"} and parts:
        return f"{host}/{parts[0].lower()}"
    labels = host.split(".")
    if len(labels) >= 2:
        return ".".join(labels[-2:])
    return host


def significance_score(article: NewsArticle) -> int:
    """Higher means more worth an engineer's time. Star count and topic are not inputs."""
    score = NOVELTY_WEIGHT[article.novelty] * 3
    score += LEVEL_WEIGHT[article.practical_significance] * 2
    score += LEVEL_WEIGHT[article.confidence]
    score += EVIDENCE_WEIGHT[article.evidence_kind]
    if article.independently_validated:
        score += 3
    return score


def select_findings(
    articles: list[NewsArticle],
    *,
    today: date | None = None,
    primary_window_days: int = 14,
    fallback_window_days: int = 30,
    min_findings: int = 5,
    max_findings: int = 10,
) -> list[NewsArticle]:
    """Keep items that pass the gate, prefer the primary window, then rank.

    The fallback window is used only when the primary window does not yield
    ``min_findings`` qualifying items. The result can be shorter than
    ``min_findings`` when the longer window is also thin.
    """
    today = today or date.today()
    qualified: list[NewsArticle] = []
    for article in articles:
        age_days = (today - article.date).days
        if age_days < 0 or age_days > fallback_window_days:
            continue
        if not article.qualifies():
            continue
        qualified.append(article)

    primary_cutoff = today - timedelta(days=primary_window_days)
    recent = [article for article in qualified if article.date >= primary_cutoff]
    pool = recent if len(recent) >= min_findings else qualified

    ranked: list[NewsArticle] = []
    for article in pool:
        copy = article.model_copy(deep=True)
        # A self-reported result is not high-confidence, even if the model said so.
        if copy.confidence == Level.high and not copy.independently_validated:
            copy.confidence = Level.medium
        ranked.append(copy)
    ranked.sort(key=lambda article: (significance_score(article), article.date), reverse=True)

    chosen: list[NewsArticle] = []
    counts: dict[str, int] = {}
    for article in ranked:
        key = project_key(article)
        if counts.get(key, 0) >= MAX_PER_PROJECT:
            continue
        chosen.append(article)
        counts[key] = counts.get(key, 0) + 1
        if len(chosen) == max_findings:
            break

    # A qualifying model release keeps a slot when other projects would otherwise fill the list.
    if not any(article.area == TechnicalArea.model_releases for article in chosen):
        release = next(
            (article for article in ranked if article.area == TechnicalArea.model_releases),
            None,
        )
        if release is not None and counts.get(project_key(release), 0) < MAX_PER_PROJECT:
            if len(chosen) < max_findings:
                chosen.append(release)
            elif chosen:
                chosen[-1] = release
            chosen.sort(
                key=lambda article: (significance_score(article), article.date),
                reverse=True,
            )

    for index, article in enumerate(chosen, start=1):
        article.rank = index
    return chosen

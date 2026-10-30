"""Rank briefing candidates by technical significance, not popularity."""

from datetime import date, timedelta

from data_model.news import EvidenceKind, Level, NewsArticle, Novelty, TechnicalArea

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
# Slight preference for the audience: agents, inference, and new mechanisms.
AREA_WEIGHT = {
    TechnicalArea.algorithms_architectures: 1,
    TechnicalArea.agentic_ai: 1,
    TechnicalArea.inference_infrastructure: 1,
    TechnicalArea.model_releases: 0,
    TechnicalArea.trending_github: 0,
    TechnicalArea.technical_interviews: 0,
}


def significance_score(article: NewsArticle) -> int:
    """Higher means more worth an engineer's time. Star count is not an input."""
    score = NOVELTY_WEIGHT[article.novelty] * 3
    score += LEVEL_WEIGHT[article.practical_significance] * 2
    score += LEVEL_WEIGHT[article.confidence]
    score += EVIDENCE_WEIGHT[article.evidence_kind]
    if article.independently_validated:
        score += 3
    score += AREA_WEIGHT[article.area]
    return score


def select_findings(
    articles: list[NewsArticle],
    *,
    today: date | None = None,
    primary_window_days: int = 7,
    fallback_window_days: int = 30,
    min_findings: int = 5,
    max_findings: int = 10,
) -> list[NewsArticle]:
    """Keep items that pass the gate, prefer the last 7 days, then rank.

    The 30-day window is used only when the last 7 days do not yield
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

    chosen = ranked[:max_findings]
    for index, article in enumerate(chosen, start=1):
        article.rank = index
    return chosen

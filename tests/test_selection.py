"""Gate and ranking rules for the technical briefing."""

from datetime import date, timedelta

from data_model.news import EvidenceKind, Level, NewsArticle, Novelty, SourceLink, TechnicalArea
from data_model.selection import select_findings


TODAY = date(2026, 10, 30)


def article(**overrides) -> NewsArticle:
    payload = {
        "title": "SGLang cascade routing",
        "source": "SGLang",
        "date": TODAY - timedelta(days=2),
        "url": "https://github.com/sgl-project/sglang/releases/tag/v0.4",
        "summary": "A serving change that overlaps prefill and decode scheduling on one engine.",
        "area": TechnicalArea.inference_infrastructure,
        "what_changed": "The scheduler overlaps prefill and decode instead of running them in separate batches.",
        "why_it_matters": "Lowers tail latency for agent loops that mix long prompts with short tool calls.",
        "evidence": "The release is in the public repository and a downstream stack adopted the scheduler flag.",
        "evidence_kind": EvidenceKind.community_adoption,
        "novelty": Novelty.meaningful,
        "practical_significance": Level.high,
        "confidence": Level.medium,
        "publicly_available": True,
        "independently_validated": True,
        "links": [
            SourceLink(
                title="Release",
                url="https://github.com/sgl-project/sglang/releases/tag/v0.4",
                kind="release_notes",
            )
        ],
    }
    payload.update(overrides)
    return NewsArticle(**payload)


def test_press_only_item_is_rejected():
    item = article(
        source="Tom's Guide",
        url="https://www.tomsguide.com/news/some-model",
        links=[],
    )
    assert select_findings([item], today=TODAY) == []


def test_press_item_with_a_repo_link_can_qualify():
    item = article(
        source="Tom's Guide",
        url="https://www.tomsguide.com/news/some-model",
        links=[
            SourceLink(
                title="Weights",
                url="https://huggingface.co/org/model",
                kind="weights",
            )
        ],
    )
    assert len(select_findings([item], today=TODAY)) == 1


def test_incremental_and_unverified_claims_are_rejected():
    incremental = article(novelty=Novelty.incremental)
    rumor = article(
        evidence_kind=EvidenceKind.developer_reported,
        independently_validated=False,
        confidence=Level.medium,
    )
    assert select_findings([incremental, rumor], today=TODAY) == []


def test_self_reported_release_cannot_keep_high_confidence():
    item = article(
        evidence_kind=EvidenceKind.primary_release,
        independently_validated=False,
        confidence=Level.high,
    )
    chosen = select_findings([item], today=TODAY)
    assert len(chosen) == 1
    assert chosen[0].confidence == Level.medium
    assert chosen[0].rank == 1


def test_recent_window_is_preferred_when_it_is_full():
    recent = [
        article(title=f"recent-{index}", url=f"https://example.com/r{index}")
        for index in range(5)
    ]
    older = article(
        title="older fundamental",
        url="https://example.com/old",
        date=TODAY - timedelta(days=20),
        novelty=Novelty.fundamental,
    )
    chosen = select_findings(recent + [older], today=TODAY, min_findings=5)
    assert len(chosen) == 5
    assert all(item.title.startswith("recent-") for item in chosen)


def test_older_items_fill_a_thin_week_and_rank_by_significance():
    recent = article(title="recent meaningful", url="https://example.com/recent")
    older = article(
        title="older fundamental",
        url="https://example.com/old",
        date=TODAY - timedelta(days=20),
        novelty=Novelty.fundamental,
        evidence_kind=EvidenceKind.independent_reproduction,
        github_stars=100000,
    )
    quiet = article(
        title="older quiet",
        url="https://example.com/quiet",
        date=TODAY - timedelta(days=18),
        novelty=Novelty.meaningful,
        practical_significance=Level.medium,
        github_stars=10,
    )
    chosen = select_findings([quiet, recent, older], today=TODAY, min_findings=5)
    assert [item.title for item in chosen] == [
        "older fundamental",
        "recent meaningful",
        "older quiet",
    ]
    assert [item.rank for item in chosen] == [1, 2, 3]


def test_trending_repo_without_a_technical_idea_is_rejected():
    item = article(
        area=TechnicalArea.trending_github,
        technical_ideas=[],
        github_stars=50000,
    )
    assert select_findings([item], today=TODAY) == []


def test_stale_and_future_items_are_rejected():
    stale = article(date=TODAY - timedelta(days=31), url="https://example.com/stale")
    future = article(date=TODAY + timedelta(days=1), url="https://example.com/future")
    assert select_findings([stale, future], today=TODAY) == []


if __name__ == "__main__":
    test_press_only_item_is_rejected()
    test_press_item_with_a_repo_link_can_qualify()
    test_incremental_and_unverified_claims_are_rejected()
    test_self_reported_release_cannot_keep_high_confidence()
    test_recent_window_is_preferred_when_it_is_full()
    test_older_items_fill_a_thin_week_and_rank_by_significance()
    test_trending_repo_without_a_technical_idea_is_rejected()
    test_stale_and_future_items_are_rejected()
    print("selection tests passed")

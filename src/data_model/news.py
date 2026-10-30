from enum import Enum
from datetime import date as Date
from typing import TypedDict
from urllib.parse import urlparse

from pydantic import BaseModel, Field, HttpUrl, field_validator

# Press and aggregator hosts are not technical primary sources.
AGGREGATOR_HOSTS = {
    "tomsguide.com",
    "techcrunch.com",
    "venturebeat.com",
    "theverge.com",
    "businessinsider.com",
    "forbes.com",
    "bloomberg.com",
    "reuters.com",
    "cnbc.com",
    "wired.com",
    "nytimes.com",
    "wsj.com",
    "ft.com",
    "theinformation.com",
}

PRIMARY_LINK_KINDS = {
    "primary",
    "repo",
    "weights",
    "release_notes",
    "docs",
    "benchmark",
    "interview",
}

AREA_LABELS = {
    "algorithms_architectures": "Algorithms & Architectures",
    "model_releases": "Model Releases",
    "agentic_ai": "Agentic AI & Harnesses",
    "inference_infrastructure": "Inference & Infrastructure",
    "trending_github": "Trending GitHub",
    "technical_interviews": "Technical Interviews",
}

EVIDENCE_LABELS = {
    "independent_reproduction": "Independent reproduction",
    "community_adoption": "Community adoption",
    "credible_benchmark": "Credible third-party benchmark",
    "substantial_open_source": "Substantial open-source implementation",
    "primary_release": "Primary release (artifact is public; numbers may be self-reported)",
    "technical_explanation": "Technical explanation with implementation detail",
    "developer_reported": "Developer-reported only",
}


class TechnicalArea(str, Enum):
    algorithms_architectures = "algorithms_architectures"
    model_releases = "model_releases"
    agentic_ai = "agentic_ai"
    inference_infrastructure = "inference_infrastructure"
    trending_github = "trending_github"
    technical_interviews = "technical_interviews"


class EvidenceKind(str, Enum):
    independent_reproduction = "independent_reproduction"
    community_adoption = "community_adoption"
    credible_benchmark = "credible_benchmark"
    substantial_open_source = "substantial_open_source"
    primary_release = "primary_release"
    technical_explanation = "technical_explanation"
    developer_reported = "developer_reported"


class Novelty(str, Enum):
    fundamental = "fundamental"
    meaningful = "meaningful"
    incremental = "incremental"


class Level(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


def host_of(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


class SourceLink(BaseModel):
    title: str = Field(description="Human-readable name of the source.")
    url: str = Field(description="Direct URL. Do not invent URLs.")
    kind: str = Field(
        description=(
            "One of: primary, repo, weights, release_notes, docs, benchmark, "
            "interview, secondary."
        )
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        HttpUrl(value)
        return value


class NewsArticle(BaseModel):
    """One candidate development for the technical intelligence briefing."""

    title: str = Field(description="Name of the model, system, repository, or talk.")
    source: str = Field(
        description="Name of the primary technical source, not a news aggregator."
    )
    date: Date = Field(description="Release or publication date from the primary source.")
    url: str = Field(description="Canonical primary URL an engineer can open.")
    summary: str = Field(
        description="Two or three sentences on the technical change. No marketing adjectives."
    )
    area: TechnicalArea
    what_changed: str = Field(
        description=(
            "The mechanism: architecture, algorithm, training method, serving technique, "
            "or harness design. State what is different from the prior approach."
        )
    )
    why_it_matters: str = Field(
        description=(
            "Impact on capability, reliability, efficiency, or engineering practice "
            "for someone building agents, evals, inference, or production infrastructure."
        )
    )
    evidence: str = Field(
        description=(
            "Specific community validation. Name the reproduction, adopter, benchmark "
            "publisher, or repo activity. Label any number the authors reported themselves "
            "as developer-reported."
        )
    )
    evidence_kind: EvidenceKind
    links: list[SourceLink] = Field(default_factory=list)
    novelty: Novelty = Field(
        description=(
            "fundamental: a new mechanism. meaningful: a real engineering method worth "
            "studying. incremental: a larger model, a UI change, or a small tuning delta."
        )
    )
    practical_significance: Level
    confidence: Level = Field(
        description=(
            "high only when an independent party reproduced or adopted the result. "
            "medium when a public artifact exists but benchmarks are self-reported. "
            "low when the claim is unverified."
        )
    )
    publicly_available: bool = Field(
        description="True only if code, weights, a shipping feature, or the full technical source is public."
    )
    independently_validated: bool = Field(
        description=(
            "True only if someone other than the author reproduced the result, "
            "published a benchmark, or adopted it in a real codebase."
        )
    )
    availability: str = Field(
        default="",
        description="How to obtain it: open weights, source repo, shipping feature, or public transcript.",
    )
    github_stars: int | None = Field(
        default=None,
        description="Current star count, only if read from GitHub. Otherwise null.",
    )
    github_recent_growth: str | None = Field(
        default=None,
        description="Verifiable recent star growth, such as '+800 stars in 7 days'. Null if unknown.",
    )
    technical_ideas: list[str] = Field(
        default_factory=list,
        description=(
            "Concrete techniques worth reading. Required for trending_github. "
            "Stars alone are not a technical idea."
        ),
    )
    rank: int | None = Field(
        default=None,
        description="Filled by the ranker after selection. Leave null when searching.",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        HttpUrl(value)
        return value

    def has_technical_source(self) -> bool:
        """True when the canonical URL or a supporting link is not a press aggregator."""
        if host_of(self.url) not in AGGREGATOR_HOSTS:
            return True
        return any(
            link.kind in PRIMARY_LINK_KINDS and host_of(link.url) not in AGGREGATOR_HOSTS
            for link in self.links
        )

    def qualifies(self) -> bool:
        """Hard gate applied after the model responds. The prompt is not the only filter."""
        if not self.publicly_available or not self.has_technical_source():
            return False
        if self.novelty == Novelty.incremental:
            return False
        if self.practical_significance == Level.low:
            return False
        if len(self.what_changed.strip()) < 40 or len(self.evidence.strip()) < 40:
            return False
        if (
            self.evidence_kind == EvidenceKind.developer_reported
            and not self.independently_validated
        ):
            return False
        if self.confidence == Level.low and not self.independently_validated:
            return False
        if self.area == TechnicalArea.trending_github and len(self.technical_ideas) == 0:
            return False
        return True


class NewsArticleList(BaseModel):
    articles: list[NewsArticle]


class CoverageMatch(BaseModel):
    """An incoming item that the repository already covers."""

    title: str
    url: str
    reason: str = Field(
        description="Which existing file covers it, and why this is not a substantial technical update."
    )


class CoverageReport(BaseModel):
    already_covered: list[CoverageMatch] = Field(default_factory=list)


class NewsArticleWithDetails(NewsArticle):
    details: str


class GraphStateNews(TypedDict):
    news: NewsArticleList

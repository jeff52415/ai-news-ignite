from pydantic import BaseModel, HttpUrl, field_validator
from datetime import date

class NewsArticle(BaseModel):
    title: str
    source: str
    date: date
    url: str
    summary: str
    
    @field_validator("url")
    def validate_url(cls, v):
        # Attempt to cast to HttpUrl — will raise if invalid
        try:
            _ = HttpUrl(v)
        except Exception:
            raise ValueError("Invalid URL format")
        return v

class NewsArticleList(BaseModel):
    articles: list[NewsArticle]

class NewsArticleWithDetails(NewsArticle):
    details: str
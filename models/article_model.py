from beanie import Document
from typing import List, Optional


class Article(Document):
    article_id: str
    title: str
    body: str
    user_id: str
    tags: List[str] = []
    score: Optional[int] = 0
    views: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "articles"


def article_to_dict(article: Article) -> dict:
    return {
        "article_id": article.article_id,
        "title": article.title,
        "body": article.body,
        "user_id": article.user_id,
        "tags": article.tags,
        "score": article.score,
        "views": article.views,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
    }

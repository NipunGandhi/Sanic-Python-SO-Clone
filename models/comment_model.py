from beanie import Document
from typing import Optional


class Comment(Document):
    comment_id: Optional[str]
    user_id: Optional[str]
    article_id: Optional[str]
    body: Optional[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "comments"


def comment_to_dict(comment: Comment) -> dict:
    return {
        "comment_id": comment.comment_id,
        "user_id": comment.user_id,
        "article_id": comment.article_id,
        "body": comment.body,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }
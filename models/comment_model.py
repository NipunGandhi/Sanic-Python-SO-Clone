from beanie import Document
from typing import Optional


class Comment(Document):
    comment_id: str
    user_id: str
    post_id: str
    body: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "comments"


def comment_to_dict(comment: Comment) -> dict:
    return {
        "comment_id": comment.comment_id,
        "user_id": comment.user_id,
        "post_id": comment.post_id,
        "article_comment": comment.article_comment,
        "question_comment": comment.question_comment,
        "body": comment.body,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }
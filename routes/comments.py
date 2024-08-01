from sanic import Blueprint, response
from sanic.request import Request
from beanie import PydanticObjectId
from models.comment_model import Comment, comment_to_dict
from datetime import datetime

comments_bp = Blueprint('comments')


@comments_bp.route("/", methods=["GET"])
async def get_comments(request: Request):
    try:
        comments = Comment.find_all()

        comments_dict = [comment_to_dict(comment) for comment in comments]
        return response.json({
            "message": "List of comments",
            "comments": comments_dict
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["GET"])
async def get_comment(request: Request, comment_id: str):
    try:
        comment = await Comment.find_one(Comment.comment_id == comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        return response.json({
            "message": "Comment details",
            "comment_id": comment_id,
            "comment": comment_to_dict(comment)
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/create", methods=["POST"])
async def create_comment(request: Request):
    try:
        data = request.json

        comment = Comment(
            comment_id=data.get('comment_id'),
            user_id=data.get('user_id'),
            post_id=data.get('post_id'),
            body=data.get('body'),
            created_at=datetime.utcnow().isoformat() + 'Z',
            updated_at=data.get('updated_at')
        )

        await comment.insert()

        return response.json({
            "message": "Comment created successfully",
            "status": "success",
            "comment": comment_to_dict(comment)
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["PUT"])
async def update_comment(request: Request, comment_id: str):
    try:
        data = request.json

        comment = await Comment.find_one(Comment.comment_id == comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        update_fields = {
            "body": data.get('body', comment.body),
            "updated_at": datetime.utcnow().isoformat() + 'Z',
            "article_comment": data.get('article_comment', comment.article_comment),
            "question_comment": data.get('question_comment', comment.question_comment)
        }

        await comment.update({"$set": {k: v for k, v in update_fields.items() if v is not None}})

        updated_comment = await Comment.get(comment_id)
        return response.json({
            "message": "Comment updated successfully",
            "status": "success",
            "comment": comment_to_dict(updated_comment)
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["DELETE"])
async def delete_comment(request: Request, comment_id: str):
    try:
        comment = await Comment.find_one(Comment.comment_id == comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        await comment.delete()

        return response.json({
            "message": "Comment deleted successfully",
            "status": "success"
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/search", methods=["GET"])
async def search_comments(request: Request):
    pass

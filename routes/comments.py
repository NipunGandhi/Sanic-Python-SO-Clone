from sanic import Blueprint, response
from sanic.request import Request
from beanie import PydanticObjectId
from utils.db import Comment
comments_bp = Blueprint('comments')


@comments_bp.route("/", methods=["GET"])
async def get_comments(request: Request):
    try:

        comments = await Comment.find_all().to_list()
        return response.json({
            "message": "List of comments",
            "comments": [comment.to_mongo().to_dict() for comment in comments]
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["GET"])
async def get_comment(request: Request, comment_id: str):
    try:

        comment_id = PydanticObjectId(comment_id)
        comment = await Comment.get(comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        return response.json({
            "message": "Comment details",
            "comment_id": comment_id,
            "comment": comment.to_mongo().to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/create", methods=["POST"])
async def create_comment(request: Request):
    try:
        data = request.json

        comment = Comment(
            user_id=data.get('user_id'),
            post_id=data.get('post_id'),
            body=data.get('body'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

        # Insert the comment into the database
        await comment.insert()

        return response.json({
            "message": "Comment created successfully",
            "status": "success",
            "comment": comment.to_mongo().to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["PUT"])
async def update_comment(request: Request, comment_id: str):
    try:
        data = request.json
        comment_id = PydanticObjectId(comment_id)

        comment = await Comment.get(comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        await comment.update({
            "$set": {
                "body": data.get('body', comment.body),
                "updated_at": data.get('updated_at', comment.updated_at)
            }
        })

        updated_comment = await Comment.get(comment_id)
        return response.json({
            "message": "Comment updated successfully",
            "status": "success",
            "comment": updated_comment.to_mongo().to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@comments_bp.route("/<comment_id>", methods=["DELETE"])
async def delete_comment(request: Request, comment_id: str):
    try:
        comment_id = PydanticObjectId(comment_id)
        comment = await Comment.get(comment_id)

        if comment is None:
            return response.json({"message": "Comment not found", "status": "error"}, status=404)

        # Delete the comment
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

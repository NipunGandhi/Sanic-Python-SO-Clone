from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

comments_bp = Blueprint('comments')


@comments_bp.route("/", methods=["GET"])
async def get_comments(request: Request):
    return json({"message": "List of comments", "comments": []})


@comments_bp.route("/<comment_id>", methods=["GET"])
async def get_comment(request: Request, comment_id: str):
    return json({"message": "Comment details", "comment_id": comment_id, "comment": {}})


@comments_bp.route("/create", methods=["POST"])
async def create_comment(request: Request):
    return json({"message": "Create a new comment", "status": "success", "comment": request.json})


@comments_bp.route("/<comment_id>", methods=["PUT"])
async def update_comment(request: Request, comment_id: str):
    return json({"message": "Update comment", "comment_id": comment_id, "updated_data": request.json})


@comments_bp.route("/<comment_id>", methods=["DELETE"])
async def delete_comment(request: Request, comment_id: str):
    return json({"message": "Delete comment", "comment_id": comment_id, "status": "success"})


@comments_bp.route("/search", methods=["GET"])
async def search_comments(request: Request):
    query = request.args.get("query", "")
    return json({"message": "Search comments", "query": query, "results": []})

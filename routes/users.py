from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

users_bp = Blueprint('users')


@users_bp.route("/", methods=["GET"])
async def get_users(request: Request):
    return json({"message": "List of users", "users": []})


@users_bp.route("/<user_id>", methods=["GET"])
async def get_user(request: Request, user_id: str):
    return json({"message": "User details", "user_id": user_id, "user": {}})


@users_bp.route("/create", methods=["POST"])
async def create_user(request: Request):
    return json({"message": "Create a new user", "status": "success", "user": request.json})


@users_bp.route("/<user_id>", methods=["PUT"])
async def update_user(request: Request, user_id: str):
    return json({"message": "Update user", "user_id": user_id, "updated_data": request.json})


@users_bp.route("/<user_id>", methods=["DELETE"])
async def delete_user(request: Request, user_id: str):
    return json({"message": "Delete user", "user_id": user_id, "status": "success"})


@users_bp.route("/<user_id>/reputation", methods=["PATCH"])
async def update_reputation(request: Request, user_id: str):
    return json({"message": "Update user reputation", "user_id": user_id, "new_reputation": request.json})


@users_bp.route("/<user_id>/profile", methods=["PATCH"])
async def update_profile(request: Request, user_id: str):
    return json({"message": "Update user profile", "user_id": user_id, "profile_data": request.json})


@users_bp.route("/search", methods=["GET"])
async def search_users(request: Request):
    query = request.args.get("query", "")
    return json({"message": "Search users", "query": query, "results": []})

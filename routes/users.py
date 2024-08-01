from beanie import Document
from sanic import Blueprint, response
from sanic.response import json
from sanic.request import Request
from utils.sequence import get_next_sequence_value
from models.user_model import User
users_bp = Blueprint('users')


@users_bp.route("/", methods=["GET"])
async def get_users(request: Request):
    try:
        # TODO: Add filters, pagination, and sort
        users_cursor = User.all()
        users = await users_cursor.to_list()

        return json({"message": "List of users", "users": users})
    except Exception as e:

        return response.json({"error": str(e)}, status=500)


@users_bp.route("/<user_id>", methods=["GET"])
async def get_user(request: Request, user_id: str):
    # TODO: Check for null
    user = await User.find_one(User.uid == user_id)

    user_dict = user.to_mongo().to_dict()

    return json({"message": "User details", "user_id": user_id, "user": user_dict})


@users_bp.route("/create", methods=["POST"])
async def create_user(request: Request):
    try:
        data = request.json

        uid = await get_next_sequence_value("user_uid")
        username = data.get('username')
        email = data.get('email')

        if not (username and email):
            return response.json({"message": "Missing required fields", "status": "error"}, status=400)

        user = User(uid=uid, username=username, email=email)

        # TODO: Check difference of insert and save [Time complexity mainly]
        await user.insert()
        user.uid = ""

        # TODO: Check how can I return map instead of this user model
        return response.json({"message": "User created successfully", "status": "success", "user": user}, )

    except Exception as e:
        return response.json({"message": str(e), "status": "error"}, status=500)


@users_bp.route("/<user_id>", methods=["PATCH"])
async def update_user(request: Request, user_id: str):
    try:
        data = request.json

        if not data:
            return response.json({"message": "Failed to parse body as JSON", "status": "error"}, status=400)

        user = await User.find_one(User.uid == user_id)

        if user is None:
            return response.json({"message": "User not found", "status": "error"}, status=404)

        user_updates = {key: value for key, value in data.items() if value is not None}

        if 'uid' in user_updates:
            del user_updates['uid']

        await user.update({"$set": user_updates})

        return response.json({"message": "User updated successfully", "status": "success", "user": "user"}, status=200)

    except Exception as e:
        return response.json({"message": str(e), "status": "error"}, status=500)


@users_bp.route("/<user_id>", methods=["DELETE"])
async def delete_user(request: Request, user_id: str):
    try:
        user = await User.find_one(User.uid == user_id)

        if user is None:
            return response.json({"message": "User not found", "status": "error"}, status=404)

        await user.delete()

        return response.json({"message": "User deleted successfully", "status": "success"}, status=200)

    except Exception as e:
        return response.json({"message": str(e), "status": "error"}, status=500)

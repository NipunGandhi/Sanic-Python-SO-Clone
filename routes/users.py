from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

users_bp = Blueprint('users')


@users_bp.route("/", methods=["GET"])
async def get_users(request: Request):
    """
    Handles requests to the "/users/" route.
    """
    return json({"message": "List of users"})


@users_bp.route("/create", methods=["POST"])
async def create_user(request: Request):
    """
    Handles requests to the "/users/post" route.
    """
    return json({"message": "Create a new user"})

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

answers_bp = Blueprint('answers')


@answers_bp.route("/", methods=["GET"])
async def get_answers(request: Request):
    return json({"message": "List of answers", "answers": []})


@answers_bp.route("/<answer_id>", methods=["GET"])
async def get_answer(request: Request, answer_id: str):
    return json({"message": "Answer details", "answer_id": answer_id, "answer": {}})


@answers_bp.route("/create", methods=["POST"])
async def create_answer(request: Request):
    return json({"message": "Create a new answer", "status": "success", "answer": request.json})


@answers_bp.route("/<answer_id>", methods=["PUT"])
async def update_answer(request: Request, answer_id: str):
    return json({"message": "Update answer", "answer_id": answer_id, "updated_data": request.json})


@answers_bp.route("/<answer_id>", methods=["DELETE"])
async def delete_answer(request: Request, answer_id: str):
    return json({"message": "Delete answer", "answer_id": answer_id, "status": "success"})


@answers_bp.route("/<answer_id>/accept", methods=["POST"])
async def accept_answer(request: Request, answer_id: str):
    return json({"message": "Accept answer", "answer_id": answer_id, "status": "success"})


@answers_bp.route("/<answer_id>/votes", methods=["PATCH"])
async def update_answer_votes(request: Request, answer_id: str):
    return json({"message": "Update answer votes", "answer_id": answer_id, "votes": request.json})


@answers_bp.route("/search", methods=["GET"])
async def search_answers(request: Request):
    query = request.args.get("query", "")
    return json({"message": "Search answers", "query": query, "results": []})

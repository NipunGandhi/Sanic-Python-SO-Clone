from sanic import Blueprint, response
from sanic.request import Request
from utils.db import Answer

answers_bp = Blueprint('answers')


@answers_bp.route("/", methods=["GET"])
async def get_answers(request: Request):
    try:
        answers = await Answer.find_all().to_list()
        return response.json({
            "message": "List of answers",
            "answers": [answer.to_dict() for answer in answers]
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/<answer_id>", methods=["GET"])
async def get_answer(request: Request, answer_id: str):
    try:
        answer = await Answer.find_one(Answer.id == answer_id)

        if answer is None:
            return response.json({"message": "Answer not found", "status": "error"}, status=404)

        return response.json({
            "message": "Answer details",
            "answer_id": answer_id,
            "answer": answer.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/create", methods=["POST"])
async def create_answer(request: Request):
    try:
        data = request.json

        answer = Answer(
            question_id=data.get('question_id'),
            user_id=data.get('user_id'),
            body=data.get('body'),
            score=data.get('score', 0),
            is_accepted=data.get('is_accepted', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

        await answer.insert()

        return response.json({
            "message": "Answer created successfully",
            "status": "success",
            "answer": answer.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/<answer_id>", methods=["PUT"])
async def update_answer(request: Request, answer_id: str):
    try:
        data = request.json

        answer = await Answer.find_one(Answer.id == answer_id)

        if answer is None:
            return response.json({"message": "Answer not found", "status": "error"}, status=404)

        answer.body = data.get('body', answer.body)
        answer.score = data.get('score', answer.score)
        answer.is_accepted = data.get('is_accepted', answer.is_accepted)
        answer.updated_at = data.get('updated_at', answer.updated_at)

        await answer.save()

        return response.json({
            "message": "Answer updated successfully",
            "status": "success",
            "answer": answer.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/<answer_id>", methods=["DELETE"])
async def delete_answer(request: Request, answer_id: str):
    try:
        answer = await Answer.find_one(Answer.id == answer_id)

        if answer is None:
            return response.json({"message": "Answer not found", "status": "error"}, status=404)

        await answer.delete()

        return response.json({
            "message": "Answer deleted successfully",
            "status": "success"
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/<answer_id>/accept", methods=["POST"])
async def accept_answer(request: Request, answer_id: str):
    try:
        answer = await Answer.find_one(Answer.id == answer_id)

        if answer is None:
            return response.json({"message": "Answer not found", "status": "error"}, status=404)

        # Mark the answer as accepted
        answer.is_accepted = True
        await answer.save()

        return response.json({
            "message": "Answer accepted successfully",
            "status": "success",
            "answer": answer.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/<answer_id>/votes", methods=["PATCH"])
async def update_answer_votes(request: Request, answer_id: str):
    try:
        data = request.json

        answer = await Answer.find_one(Answer.id == answer_id)

        if answer is None:
            return response.json({"message": "Answer not found", "status": "error"}, status=404)

        votes = data.get('votes')
        if votes is not None:
            answer.score = votes

        await answer.save()

        return response.json({
            "message": "Answer votes updated successfully",
            "status": "success",
            "answer": answer.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@answers_bp.route("/search", methods=["GET"])
async def search_answers(request: Request):
    try:
       pass
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

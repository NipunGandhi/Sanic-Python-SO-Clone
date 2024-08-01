from sanic import Blueprint, response
from sanic.request import Request
from typing import List, Optional
from pydantic import BaseModel
from utils.db import Question
questions_bp = Blueprint('questions')


class QuestionCreate(BaseModel):
    title: str
    body: str
    user_id: str
    tags: Optional[List[str]] = []
    score: Optional[int] = 0
    views: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: Optional[str] = 'open'


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None
    score: Optional[int] = None
    views: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: Optional[str] = None


@questions_bp.route("/", methods=["GET"])
async def get_questions(request: Request):
    try:
        questions_cursor = Question.all()
        questions = await questions_cursor.to_list()
        return response.json({"message": "List of questions", "questions": questions})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/<question_id>", methods=["GET"])
async def get_question(request: Request, question_id: str):
    try:
        question = await Question.get(question_id)
        if question is None:
            return response.json({"message": "Question not found", "status": "error"}, status=404)
        return response.json({"message": "Question details", "question_id": question_id, "question": question})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/create", methods=["POST"])
async def create_question(request: Request):
    try:
        data = request.json
        question_data = QuestionCreate(**data)

        question = Question(
            title=question_data.title,
            body=question_data.body,
            user_id=question_data.user_id,
            tags=question_data.tags,
            score=question_data.score,
            views=question_data.views,
            created_at=question_data.created_at,
            updated_at=question_data.updated_at,
            status=question_data.status
        )

        await question.insert()
        return response.json({"message": "Question created successfully", "status": "success", "question": question})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/<question_id>", methods=["PUT"])
async def update_question(request: Request, question_id: str):
    try:
        data = request.json
        update_data = QuestionUpdate(**data)
        question = await Question.get(question_id)

        if question is None:
            return response.json({"message": "Question not found", "status": "error"}, status=404)

        if update_data.title is not None:
            question.title = update_data.title
        if update_data.body is not None:
            question.body = update_data.body
        if update_data.tags is not None:
            question.tags = update_data.tags
        if update_data.score is not None:
            question.score = update_data.score
        if update_data.views is not None:
            question.views = update_data.views
        if update_data.created_at is not None:
            question.created_at = update_data.created_at
        if update_data.updated_at is not None:
            question.updated_at = update_data.updated_at
        if update_data.status is not None:
            question.status = update_data.status

        await question.save()
        return response.json({"message": "Question updated successfully", "status": "success", "question": question})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/<question_id>", methods=["DELETE"])
async def delete_question(request: Request, question_id: str):
    try:
        question = await Question.get(question_id)
        if question is None:
            return response.json({"message": "Question not found", "status": "error"}, status=404)

        await question.delete()
        return response.json({"message": "Question deleted successfully", "status": "success"})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/<question_id>/answers", methods=["GET"])
async def get_answers_for_question(request: Request, question_id: str):
    try:
        # TODO: Check logic
        return response.json(
            {"message": "List of answers for question", "question_id": question_id, "answers": answers})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@questions_bp.route("/search", methods=["GET"])
async def search_questions(request: Request):
    query = request.args.get("query", "")
    try:
        # TODO: Update
        return response.json({"message": "Search questions", "query": query, "results": questions})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

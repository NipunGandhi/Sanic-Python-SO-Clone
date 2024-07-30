from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

articles_bp = Blueprint('articles')


@articles_bp.route("/", methods=["GET"])
async def get_articles(request: Request):
    return json({"message": "List of articles", "articles": []})


@articles_bp.route("/<article_id>", methods=["GET"])
async def get_article(request: Request, article_id: str):
    return json({"message": "Article details", "article_id": article_id, "article": {}})


@articles_bp.route("/create", methods=["POST"])
async def create_article(request: Request):
    return json({"message": "Create a new article", "status": "success", "article": request.json})


@articles_bp.route("/<article_id>", methods=["PUT"])
async def update_article(request: Request, article_id: str):
    return json({"message": "Update article", "article_id": article_id, "updated_data": request.json})


@articles_bp.route("/<article_id>", methods=["DELETE"])
async def delete_article(request: Request, article_id: str):
    return json({"message": "Delete article", "article_id": article_id, "status": "success"})


@articles_bp.route("/search", methods=["GET"])
async def search_articles(request: Request):
    query = request.args.get("query", "")
    return json({"message": "Search articles", "query": query, "results": []})


@articles_bp.route("/<article_id>/comments", methods=["GET"])
async def get_comments_for_article(request: Request, article_id: str):
    return json({"message": "List of comments for article", "article_id": article_id, "comments": []})

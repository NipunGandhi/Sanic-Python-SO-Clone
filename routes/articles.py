from sanic import Blueprint, response
from sanic.request import Request
from utils.db import User
from models.article_model import Article, article_to_dict
from utils.sequence import get_next_sequence_value
from datetime import datetime

articles_bp = Blueprint('articles')


@articles_bp.route("/", methods=["GET"])
async def get_articles(request: Request):
    try:
        articles = await Article.find_all().to_list()
        articles_dict = [article_to_dict(article) for article in articles]
        return response.json({
            "message": "List of articles",
            "articles": articles_dict
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/<article_id>", methods=["GET"])
async def get_article(request: Request, article_id: str):
    try:
        article = await Article.find_one(Article.article_id == article_id)
        if article is None:
            return response.json({"message": "Article not found", "status": "error"}, status=404)

        article_dict = article_to_dict(article)
        return response.json({
            "message": "Article details",
            "article_id": article_id,
            "article": article_dict
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/create", methods=["POST"])
async def create_article(request: Request):
    try:
        data = request.json
        user = await User.find_one(User.uid == data.get('user_id'))

        if user is None:
            raise Exception("Invalid UID")

        article_id = await get_next_sequence_value(sequence_name="article_id", suffix="AID")

        article = Article(
            article_id=article_id,
            title=data.get('title'),
            body=data.get('body'),
            user_id=data.get('user_id'),
            tags=data.get('tags', []),
            created_at=datetime.utcnow().isoformat() + 'Z',
        )

        await article.insert()

        article_dict = article_to_dict(article)
        return response.json({
            "message": "Article created successfully",
            "status": "success",
            "article": article_dict
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/<article_id>", methods=["PUT"])
async def update_article(request: Request, article_id: str):
    try:
        data = request.json
        article = await Article.find_one(Article.article_id == article_id)

        if article is None:
            return response.json({"message": "Article not found", "status": "error"}, status=404)

        article.title = data.get('title', article.title)
        article.body = data.get('body', article.body)
        article.tags = data.get('tags', article.tags)
        article.score = data.get('score', article.score)
        article.views = data.get('views', article.views)
        article.updated_at = data.get('updated_at', article.updated_at)

        await article.save()

        article_dict = article_to_dict(article)
        return response.json({
            "message": "Article updated successfully",
            "status": "success",
            "article": article_dict
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/<article_id>", methods=["DELETE"])
async def delete_article(request: Request, article_id: str):
    try:
        article = await Article.find_one(Article.article_id == article_id)

        if article is None:
            return response.json({"message": "Article not found", "status": "error"}, status=404)

        await article.delete()

        return response.json({
            "message": "Article deleted successfully",
            "status": "success"
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/search", methods=["GET"])
async def search_articles(request: Request):
    try:
        pass
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/<article_id>/comments", methods=["GET"])
async def get_comments_for_article(request: Request, article_id: str):
    try:
        pass
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

from sanic import Blueprint, response
from sanic.request import Request
from db import Article

articles_bp = Blueprint('articles')


@articles_bp.route("/", methods=["GET"])
async def get_articles(request: Request):
    try:
        articles = await Article.find_all().to_list()
        return response.json({
            "message": "List of articles",
            "articles": [article.to_dict() for article in articles]
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/<article_id>", methods=["GET"])
async def get_article(request: Request, article_id: str):
    try:
        article = await Article.find_one(Article.article_id == article_id)

        if article is None:
            return response.json({"message": "Article not found", "status": "error"}, status=404)

        return response.json({
            "message": "Article details",
            "article_id": article_id,
            "article": article.to_dict()
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@articles_bp.route("/create", methods=["POST"])
async def create_article(request: Request):
    try:
        data = request.json

        article_id = data.get('article_id')

        article = Article(
            article_id=article_id,
            title=data.get('title'),
            body=data.get('body'),
            user_id=data.get('user_id'),
            tags=data.get('tags', []),
            score=data.get('score', 0),
            views=data.get('views', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

        await article.insert()

        return response.json({
            "message": "Article created successfully",
            "status": "success",
            "article": article.to_dict()
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

        return response.json({
            "message": "Article updated successfully",
            "status": "success",
            "article": article.to_dict()
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

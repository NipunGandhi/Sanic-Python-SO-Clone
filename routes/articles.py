from sanic import Blueprint
from sanic.response import json

# Create a Blueprint for article-related routes
articles_bp = Blueprint('articles')

@articles_bp.route("/")
async def get_articles(request):
    """
    Handles requests to the "/articles/" route.
    """
    return json({"message": "List of articles"})

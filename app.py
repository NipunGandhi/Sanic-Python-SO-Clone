from sanic import Sanic
from sanic.response import json
import logging
from sanic.exceptions import NotFound

from utils.db import init_db
from routes.users import users_bp
from routes.articles import articles_bp
from routes.answers import answers_bp
from routes.comments import comments_bp
from routes.questions import questions_bp

from utils.rate_limiter import initialize_and_increment_counter, get_request_count

app = Sanic("MySanicApp")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.before_server_start
async def setup_database(app, loop):
    await init_db()


@app.middleware('request')
async def middleware_increment_counter(request):
    initialize_and_increment_counter(request)


app.blueprint(users_bp, url_prefix='/users')
app.blueprint(articles_bp, url_prefix='/articles')
app.blueprint(comments_bp, url_prefix='/comments')
app.blueprint(questions_bp, url_prefix='/questions')
app.blueprint(answers_bp, url_prefix='/answers')


@app.exception(NotFound)
async def handle_not_found(request, exception):
    logger.error("404 Not Found: %s", request.path)
    return json({"error": "Resource not found"}, status=404)


@app.exception(Exception)
async def handle_generic_exception(request, exception):
    logger.error("500 Internal Server Error: %s", str(exception))
    return json({"error": "Internal server error"}, status=500)


@app.get('/stats')
async def get_stats(request):
    count = get_request_count(request)
    return json({"total_requests": count})


if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]

    logger.info("Starting Sanic app on port %d with debug=%s", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)

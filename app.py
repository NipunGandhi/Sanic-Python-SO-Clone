from sanic import Sanic
from sanic.response import json
import logging
from sanic.exceptions import NotFound

# Import blueprints
from routes.users import users_bp
from routes.articles import articles_bp

from counter import initialize_and_increment_counter, get_request_count

# Create the Sanic app instance
app = Sanic("MySanicApp")

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Middleware to initialize and increment request counter
@app.middleware('request')
async def middleware_increment_counter(request):
    val = initialize_and_increment_counter(request)
    if not val:
        return json({"error": "Limit reached"}, status=404)


# Register blueprints
app.blueprint(users_bp, url_prefix='/users')
app.blueprint(articles_bp, url_prefix='/articles')


# Handle 404 Not Found errors
@app.exception(NotFound)
async def handle_not_found(request, exception):
    logger.error("404 Not Found: %s", request.path)
    return json({"error": "Resource not found"}, status=404)


# Handle general exceptions
@app.exception(Exception)
async def handle_generic_exception(request, exception):
    logger.error("500 Internal Server Error: %s", str(exception))
    return json({"error": "Internal server error"}, status=500)


# Route to get the request count
@app.get('/stats')
async def get_stats(request):
    count = get_request_count(request)
    return json({"total_requests": count})


# Run the Sanic application
if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]

    logger.info("Starting Sanic app on port %d with debug=%s", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)

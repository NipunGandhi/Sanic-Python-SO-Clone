from sanic import json

MAX_LIMIT = 10


def initialize_and_increment_counter(request):
    if not hasattr(request.conn_info.ctx, "call_count"):
        request.conn_info.ctx.call_count = 0

    if not request.conn_info.ctx.call_count < MAX_LIMIT:
        request.conn_info.ctx.call_count += 1
        return json({"error": "Limit reached"}, status=404)


def get_request_count(request):
    return getattr(request.conn_info.ctx, "call_count", 0)

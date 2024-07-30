# Define a maximum limit for the request count
MAX_LIMIT = 10


def initialize_and_increment_counter(request):
    if not hasattr(request.conn_info.ctx, "call_count"):
        request.conn_info.ctx.call_count = 0

    if request.conn_info.ctx.call_count < MAX_LIMIT:
        request.conn_info.ctx.call_count += 1
        return True
    else:
        return False


def get_request_count(request):
    return getattr(request.conn_info.ctx, "call_count", 0)

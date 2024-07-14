import logging
from app.request_handler.get import GetRequestHandler
from app.request_handler.post import PostRequestHandler

logger = logging.getLogger(__name__)
logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_requests(func):
    def logger_wrapper(*args, **kwargs):
        logger.info('Request Logging Started')
        request = func(*args, **kwargs)
        logger.info('Request: %s', request)
        logger.info('*' * 50)
        return request
    return logger_wrapper

def authorize_request(func):
    def check_auth(*args, **kwargs):
        router = args[1]
        request = func(*args, **kwargs)
        if "POST" in request:
            request_handler = PostRequestHandler(request_text=request)
        elif "GET" in request:
            request_handler = GetRequestHandler(request_text=request)
        else:
            return request, False, "Server only accepts GET and POST requests"
        val, message = request_handler.validate_request()
        if val == False:
            return request, val, message
        path = request_handler.http_request_line["path"]
        method = request_handler.http_request_line["method"]
        if path in router.routes.keys() and router.routes[path]["route"].method == method:
            route = router.routes[path]["route"]
        else:
            return request, False, "Route not found"
        if route.needs_auth:
            val, message = request_handler.validate_authorization()
            if not val:
                message = "Authorization Error: " + message
        return request, val, message
    return check_auth





import asyncio
from app.request_handler.get import GetRequestHandler
from app.request_handler.post import PostRequestHandler
from app.response_handler.response_handler import ResponseHandler
from app.generators.generators import streaming_response_generator

class AsyncRequestIterator:
    def __init__(self, router):
        self.router = router
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        request_data = self.router.process_request()
        if request_data:
            http_request_line, headers, body, request = request_data
            routes = self.router.routes
            response = await self.pass_to_handler(request, routes, http_request_line, headers, body)
            return response
        else:
            raise StopAsyncIteration
    
    async def pass_to_handler(self, request, routes, http_request_line, headers, body):
        method = http_request_line["method"]
        URL = http_request_line["path"]
        if URL in routes.keys():
            func = routes[URL]["func"]
            route_object = routes[URL]["route"]
            streaming = route_object.streaming
            needs_auth = route_object.needs_auth
            if route_object.method == "GET" and method == "GET":
                handler = GetRequestHandler(request_text=request, needs_auth=needs_auth, streaming=streaming)
            elif route_object.method == "POST" and method == "POST":
                handler = PostRequestHandler(request_text=request, needs_auth=needs_auth, streaming=streaming)
            return await handler.handle_request(func)
        else:
            response = ResponseHandler(
                http_version="HTTP/1.1",
                status_code="404 Not Found",
                headers={"Content-Length": "0"},
                body=""
            )
            return streaming_response_generator(response)

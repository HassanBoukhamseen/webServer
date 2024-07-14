from app.request_handler.base import BaseRequestHandler
from app.generators.generators import streaming_response_generator
from app.response_handler.response_handler import ResponseHandler

class PostRequestHandler(BaseRequestHandler):
    def __init__(self, request_text=None, needs_auth=False, streaming=False):
        super().__init__(
            request_text, 
            needs_auth,
            streaming
        )
        
    async def handle_request(self, func):
        result = func()
        if self.streaming:
            response = ResponseHandler(
                http_version="HTTP/1.1",
                status_code="200 OK",
                headers={
                    "Content-Type": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                },
                body=result
            )
            return streaming_response_generator(response)
        else:
            response = ResponseHandler(
                http_version="HTTP/1.1",
                status_code="200 OK",
                headers={
                    "Content-Length": f"{len(result)}",
                },
                body=result
            )
            return response
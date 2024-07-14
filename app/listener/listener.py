import socket
import asyncio
import random
from collections import defaultdict
from app.router.router import Router
from app.iterators.iterators import AsyncRequestIterator
from app.response_handler.response_handler import ResponseHandler
from app.decorators.decorators import log_requests, authorize_request
from app.rate_limiter.rate_limiter import RateLimiter

class Listener:
    def __init__(self, host='127.0.0.1', port=8080, router=Router(), max_requests=15, time_window=60):
        self.host = host
        self.port = port
        self.router = router
        self.rate_limiter = RateLimiter(max_requests, time_window)

    async def connect_to_client(self):
        try:
            print(f"Connected to {self.client_address}")
            client_id = self.client_address[0]

            if not self.rate_limiter.is_allowed(client_id):
                response = ResponseHandler(
                    http_version="HTTP/1.1",
                    status_code="429 Too Many Requests",
                    headers={},
                    body={"error": "Too Many Requests", "message": "Rate limit exceeded"}
                )
                self.client_socket.sendall(str(response).encode('utf-8'))
                return

            request, val, message = self.recieve_requests(self.router)
            if not val:
                status_code = "401 Unauthorized" if "Authorization Error" in message else "400 Bad Request"
                error = "Unauthorized" if "Authorization Error" in message else "Bad Request"
                response = ResponseHandler(
                    http_version="HTTP/1.1",
                    status_code=status_code,
                    headers={},
                    body={"error": error, "message": message}
                )
                self.client_socket.sendall(str(response).encode('utf-8'))
            else:
                self.router.add_request(request)
                async for output in AsyncRequestIterator(self.router):
                    if type(output) == ResponseHandler:
                        self.client_socket.sendall(str(output).encode('utf-8'))
                    else:
                        for response_part in output:
                            self.client_socket.sendall(response_part.encode('utf-8'))
                            delay = random.randint(1, 3)
                            await asyncio.sleep(delay/10)
        except Exception as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            self.close()

    @log_requests
    @authorize_request
    def recieve_requests(self, router):
        return self.client_socket.recv(4096).decode('utf-8')
    
    def close(self):
        self.client_socket.close()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server is listening on {self.host}:{self.port}")

            while True:
                self.client_socket, self.client_address = server_socket.accept()
                asyncio.run(self.connect_to_client())


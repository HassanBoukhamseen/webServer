import json

class Route:
    def __init__(self, URL, method, needs_auth, streaming):
        self.URL = URL
        self.method = method
        self.needs_auth = needs_auth
        self.streaming = streaming

class Router:
    def __init__(self, request_queue=[]):
        self.routes = {}
        self.request_queue = request_queue

    def add(self, URL, method, needs_auth, streaming):
        def decorator(func):
            route = Route(URL=URL, method=method, needs_auth=needs_auth, streaming=streaming)
            if route.URL not in self.routes.keys():
                self.routes[route.URL] = {"route": route, "func": func}
            else:
                raise ValueError(f"This route is already defined for request type {method}")
            return func
        return decorator
    
    def add_request(self, request):
        self.request_queue.append(request)
    
    def parse_request_text(self, request):
        lines = request.split('\r\n')
        request_line = lines[0].split(' ')
        method = request_line[0]
        path = request_line[1]
        http_version = request_line[2]
        headers = {}
        body = None
        is_body = False
        body_lines = []
        for line in lines[1:]:
            if is_body:
                body_lines.append(line)
            elif line == '':
                is_body = True
            else:
                header_key, header_value = line.split(': ', 1)
                headers[header_key] = header_value
        if body_lines:
            body_str = '\n'.join(body_lines).strip()
            try:
                body = json.loads(body_str)
            except json.JSONDecodeError:
                body = body_str
        
        http_request_line = {
            'method': method,
            'path': path,
            'http_version': http_version
        }
        return http_request_line, headers, body
    
    def process_request(self):
        if len(self.request_queue) != 0:
            request = self.request_queue.pop(0)
            http_request_line, headers, body = self.parse_request_text(request)
            return http_request_line, headers, body, request
        return None
        
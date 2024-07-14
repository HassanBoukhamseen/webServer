from abc import ABC, abstractmethod
import json
import base64

HTTP_METHODS = {"GET", "POST"}

class BaseRequestHandler(ABC):
    def __init__(self, request_text, needs_auth=False, streaming=False):
        self.needs_auth = needs_auth
        self.streaming = streaming
        if request_text:
            self.request_text = request_text
            self.http_request_line, self.headers, self.body = self.parse_request_text()
        else:
            raise ValueError("Request passed is None")
    
    def parse_request_text(self):
        lines = self.request_text.split('\r\n')
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

    def format_request(self):
        request_line = f"{self.http_request_line['method']} {self.http_request_line['path']} {self.http_request_line['http_version']}"
        headers = "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()])
        if isinstance(self.body, dict):
            body = json.dumps(self.body)
        else:
            body = self.body
        request = f"{request_line}\r\n{headers}\r\n\r\n{body}"
        return request

    def __repr__(self):
        if not hasattr(self, 'request_text'):
            self.request_text = self.format_request()
        return self.request_text

    def validate_request(self):
        lines = self.request_text.split('\r\n')
        
        is_valid, message = self.validate_request_line(lines)
        if not is_valid:
            return is_valid, message
        
        method, path, http_version = lines[0].split(' ')
        
        is_valid, message = self.validate_method(method)
        if not is_valid:
            return is_valid, message
        
        is_valid, message = self.validate_http_version(http_version)
        if not is_valid:
            return is_valid, message
        
        headers, body_lines, is_valid, message = self.parse_headers_and_body(lines)
        if not is_valid:
            return is_valid, message
        
        if method == "POST":
            is_valid, message = self.validate_post_request(headers, body_lines)
            if not is_valid:
                return is_valid, message
        elif method == "GET":
            is_valid, message = self.validate_get_request(body_lines)
            if not is_valid:
                return is_valid, message
        if self.needs_auth:
            is_valid, message = self.validate_authorization()
            if not is_valid:
                return is_valid, "Authorization Error: " + message
            
        return True, "Request is valid"

    def validate_request_line(self, lines):
        if not lines or len(lines) < 1:
            return False, "Missing HTTP request line"
        
        request_line = lines[0].split(' ')
        if len(request_line) != 3:
            return False, "Invalid HTTP request line format"
        
        return True, "Request line is valid"
    
    def validate_authorization(self):
        if "Authorization" not in self.headers:
            return False, "Authorization header is missing"
        auth_header = self.headers["Authorization"]
        if auth_header.startswith("Basic "):
            try:
                auth_str = base64.b64decode(auth_header[6:]).decode('utf-8')
                username, password = auth_str.split(':')
                print(username, password)
                if username == "Hassan" and password == "Anzor": 
                    return True, "Authorization is valid"
                else:
                    return False, "Invalid Basic authentication credentials"
            except Exception as e:
                return False, f"Error in Basic authentication: {e}"
        elif auth_header.startswith("Bearer "):
            token = auth_header[7:]
            if token == "pwc_is_the_best_of_the_top_4":
                return True, "Authorization is valid"
            else:
                return False, "Invalid Bearer token"
        elif auth_header.startswith("Api-Key "):
            api_key = auth_header[8:]
            if api_key == "0545229090":
                return True, "Authorization is valid"
            else:
                return False, "Invalid API key"
        
        else:
            return False, "Unsupported Authorization type"

    def validate_method(self, method):
        if method not in HTTP_METHODS:
            return False, f"Invalid HTTP method: {method}. Supported methods are GET and POST"
        
        return True, "Method is valid"

    def validate_http_version(self, http_version):
        if not http_version.startswith("HTTP/"):
            return False, "Invalid HTTP version"
        
        return True, "HTTP version is valid"

    def parse_headers_and_body(self, lines):
        headers = {}
        is_body = False
        body_lines = []
        
        for line in lines[1:]:
            if is_body:
                body_lines.append(line)
            elif line == '':
                is_body = True
            else:
                if ': ' not in line:
                    return headers, body_lines, False, f"Invalid header format: {line}"
                header_key, header_value = line.split(': ', 1)
                headers[header_key] = header_value
        
        return headers, body_lines, True, "Headers and body parsed successfully"

    def validate_post_request(self, headers, body_lines):
        if 'Content-Type' in headers and 'application/json' not in headers['Content-Type']:
            return False, "Content-Type must be application/json for POST requests"
        
        body = '\n'.join(body_lines).strip()
        if body:
            try:
                json.loads(body)
            except json.JSONDecodeError:
                return False, "Body must be valid JSON"
        
        return True, "POST request is valid"

    def validate_get_request(self, body_lines):
        body = '\n'.join(body_lines).strip()
        if body:
            return False, "GET request should not have a body"
        
        return True, "GET request is valid"
    
    @abstractmethod
    def handle_request(self):
        pass
    


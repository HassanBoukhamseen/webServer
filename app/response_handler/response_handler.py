import json

class ResponseHandler:
    def __init__(self, http_version=None, status_code=None, headers=None, body=None):
        if all([http_version, status_code, headers is not None, body is not None]):
            self.http_version = http_version
            self.status_code = status_code
            self.headers = headers
            self.body = body
        else:
            raise ValueError("Invalid initialization parameters.")

    def format_response(self):
        status_line = f"{self.http_version} {self.status_code}"
        headers = "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()])
        response = f"{status_line}\r\n{headers}\r\n\r\n{self.body}"
        return response

    def __repr__(self):
        self.response_text = self.format_response()
        return self.response_text

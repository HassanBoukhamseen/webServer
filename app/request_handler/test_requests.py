import unittest
from app.request_handler.get import GetRequestHandler
from app.request_handler.post import PostRequestHandler

class TestRequestHandlers(unittest.TestCase):
    def test_wrong_method(self):
        request = GetRequestHandler(request_text='''DELETE /some/route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4''')
        val, text = request.validate_request()
        correct = (
            False, 
            "Invalid HTTP method: DELETE. Supported methods are GET and POST"
        )
        self.assertEqual((val, text), correct)

    def test_wrong_content_type(self):
        request = PostRequestHandler(request_text='''POST /api/resource HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4\r\nContent-Type: text/plain\r\nContent-Length: 18\r\n\r\nThis is a test.''')
        correct = (
            False, 
            "Content-Type must be application/json for POST requests"
        )
        val, text = request.validate_request()
        self.assertEqual((val, text), correct)

    def test_correct_get(self):
        request = GetRequestHandler(request_text='''GET /api/resource HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4''')
        correct = (
            True, 
            "Request is valid"
        )
        val, text = request.validate_request()
        self.assertEqual((val, text), correct)

    def test_correct_post(self):
        request = PostRequestHandler(request_text='''POST /api/resource HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4\r\nContent-Type: application/json\r\nContent-Length: 18\r\n\r\n{"key":"value"}''')
        correct = (
            True, 
            "Request is valid"
        )
        val, text = request.validate_request()
        self.assertEqual((val, text), correct)

    def test_parse_get(self):
        request = GetRequestHandler(request_text='''GET /api/resource HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4''')
        correct = (
            {'http_version': 'HTTP/1.1', 'method': 'GET', 'path': '/api/resource'}, 
            {'Authorization': 'Bearer pwc_is_the_best_of_the_top_4', 'Host': 'example.com'}, 
            None
        )
        test = request.http_request_line, request.headers, request.body
        self.assertEqual(test, correct)
    
    def test_parse_post(self):
        request_text = '''POST /api/resource HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4\r\nContent-Type: application/json\r\nContent-Length: 18\r\n\r\n{"key":"value"}'''
        request = PostRequestHandler(request_text=request_text)
        correct = (
            {'http_version': 'HTTP/1.1', 'method': 'POST', 'path': '/api/resource'}, 
            {'Authorization': 'Bearer pwc_is_the_best_of_the_top_4', 'Host': 'example.com', 'Content-Type': 'application/json','Content-Length': '18'}, 
            {"key":"value"}
        )
        test = request.http_request_line, request.headers, request.body
        self.assertEqual(test, correct)

if __name__ == '__main__':
    unittest.main()


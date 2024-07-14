import unittest
from app.decorators.decorators import log_requests, authorize_request
from app.router.router import Router
import base64

class TestDecorators(unittest.TestCase):
    def test_log_requests(self):
        @log_requests
        def sample_request():
            return '''GET /some/route HTTP/1.1\r\nHost: hassan.com'''
        sample_request()
        with open("requests.log") as log:
            self.assertIsNot(len(log.readlines()), 0)
    
    def test_authorize_request_valid_bearer(self):
        dummy_input = ""  
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            return '''GET /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4''' 
        
        @authorize_request
        def   sample_request(dummy_input, router):
            return foo()
        try:
              sample_request(dummy_input, router)
        except ValueError:
            self.fail("authorize_request raised ValueError unexpectedly!")
    
    def test_authorize_request_valid_basic(self): 
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            encoded_credentials = base64.b64encode(b"Hassan:Anzor").decode("utf-8")
            return f'''GET /some/route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Basic {encoded_credentials}'''
               
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        try:
            sample_request(dummy_input, router)
        except ValueError:
            self.fail("authorize_request raised ValueError unexpectedly!")
    
    def test_authorize_request_valid_api_key(self):  
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            return '''GET /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Api-Key 0545229090'''
               
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        try:
            sample_request(dummy_input, router)
        except ValueError:
            self.fail("authorize_request raised ValueError unexpectedly!")
    
    def test_authorize_request_invalid_method(self):
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            return '''DELETE /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Bearer pwc_is_the_best_of_the_top_4'''
        
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        _, val, message = sample_request(dummy_input, router)
        correct = (
            False,
            "Server only accepts GET and POST requests"
        )
        self.assertEqual(correct, (val, message))
    
    def test_authorize_request_invalid_auth_bearer(self):
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            return '''GET /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Bearer somethingInvalid'''
        
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        _, val, message = sample_request(dummy_input, router)
        correct = (
            False,
            "Authorization Error: Invalid Bearer token"
        )
        self.assertEqual(correct, (val, message))
    
    def test_authorize_request_invalid_auth_basic(self):
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            encoded_credentials = base64.b64encode(b"someUser:wrongPass").decode("utf-8")
            return f'''GET /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Basic {encoded_credentials}'''
        
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        _, val, message = sample_request(dummy_input, router)
        correct = (
            False,
            "Authorization Error: Invalid Basic authentication credentials"
        )
        self.assertEqual(correct, (val, message))
    
    def test_authorize_request_invalid_auth_api_key(self):
        dummy_input = ""
        router = Router()
        @router.add("/some_route", method="GET", needs_auth=True, streaming=False)
        def foo():
            return '''GET /some_route HTTP/1.1\r\nHost: hassan.com\r\nAuthorization: Api-Key 1000000'''
        
        @authorize_request
        def sample_request(dummy_input, router):
            return foo()
        _, val, message = sample_request(dummy_input, router)
        correct = (
            False,
            "Authorization Error: Invalid API key"
        )
        self.assertEqual(correct, (val, message))

if __name__ == '__main__':
    unittest.main()

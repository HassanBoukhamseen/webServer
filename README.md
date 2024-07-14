# Server Library

## Overview
The `WebServer` module provides a robust framework for creating and managing a web server with features such as streaming responses, asynchronous request processing, and request routing. It is designed to handle HTTP GET and POST requests efficiently, with support for request logging and authorization.

## Usage Example
Below is an example of how to use the `WebServer` module to set up and run a web server.

```python
from webserver import WebServer
from test_text import text
from app.context_manager.context_manager import ServerContextManager

def main():
    port = 8080
    webserver = WebServer(port=port)

    @webserver.router.add('/needs_auth', 'GET', needs_auth=True)
    def needs_auth():
        return "This is a response for a request that needs authentication"

    @webserver.router.add('/sample_post', 'POST', needs_auth=False)
    def handle_post():
        return "This is a POST response"
    webserver.listen()

if __name__ == "__main__":
    main()
```
## Explanation of the Example Code

- Routes are added using the `@webserver.router.add` decorator. Each route specifies the URL, HTTP method, and whether authentication is required.
- The `needs_auth` parameter in the route decorator determines if a route requires authentication.
- The server is run by creating an instance of the `WebServer` class and calling its `listen()` method.

## Running the Server

To run the server, execute the `main.py` file:

```sh
python3 main.py
```

## Running the Tests
to run the test script, run
```sh
chmod +x run_test.sh
./run_tests.sh
```

## Testing the Routes
To test all three routes shown in the example usage code, use the following curl requests:

 - GET request to /needs_auth with correct authentication:
```sh
curl -H "Authorization: Basic $(echo -n '<USER>:<PASSWORD>' | base64)" http://127.0.0.1:8080/needs_auth
```
where the user and the password are hardcoded in the app/request_handler/base.py file

 - POST request to /sample_post
```sh
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" http://127.0.0.1:8080/sample_post
```
 - GET request to /sample_get (streamed response)
```sh
curl -X GET http://127.0.0.1:8080/sample_get
```

## Modules

- [WebServer](https://github.com/HassanBoukhamseen/webServer/blob/main/webserver.py): Provides the main server configuration and management functionalities, including starting and stopping the server.
- [Router](https://github.com/HassanBoukhamseen/webServer/blob/main/app/router/router.py): Manages request routing by defining routes and handling incoming requests.
- [Listener](https://github.com/HassanBoukhamseen/webServer/blob/main/app/listener/listener.py): Handles incoming connections and delegates them to the appropriate router for processing.
- [AsyncRequestIterator](https://github.com/HassanBoukhamseen/webServer/blob/main/app/iterators/iterators.py): Asynchronously iterates over incoming HTTP requests and processes them based on the route and method.
- [Request Handlers](https://github.com/HassanBoukhamseen/webServer/tree/main/app/request_handler): Provides classes for handling specific HTTP request methods, such as GET and POST.
- [Response Handler](https://github.com/HassanBoukhamseen/webServer/blob/main/app/response_handler/response_handler.py): Formats HTTP responses, encapsulating the HTTP version, status code, headers, and body.
- [Decorators](https://github.com/HassanBoukhamseen/webServer/blob/main/app/decorators/decorators.py): Adds additional functionality to the request handling process, such as logging and authorization.
- [Generators](https://github.com/HassanBoukhamseen/webServer/blob/main/app/generators/generators.py): Handles the streaming of responses in chunks.
- [Context Managers](https://github.com/HassanBoukhamseen/webServer/blob/main/app/context_manager/context_manager.py): Manages the lifecycle of the web server, ensuring it starts and stops appropriately.

For more the implementation of each module, please refer to the source files in the respective directories. The documentation can be accessed at [documentation](https://github.com/HassanBoukhamseen/webServer/blob/main/server_documentation.pdf)

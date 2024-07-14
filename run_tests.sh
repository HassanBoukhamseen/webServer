#!/bin/bash

# Run the decorator tests
echo "Running decorator tests..."
python3 -m app.decorators.decorator_test
if [ $? -ne 0 ]; then
    echo "Decorator tests failed!"
    exit 1
fi

# Run the request handler tests
echo "Running request handler tests..."
python3 -m app.request_handler.test_requests
if [ $? -ne 0 ]; then
    echo "Request handler tests failed!"
    exit 1
fi

# Run the web server tests
echo "Running web server tests..."
python3 -m test_webserver
if [ $? -ne 0 ]; then
    echo "Web server tests failed!"
    exit 1
fi

echo "All tests passed successfully!"
exit 0

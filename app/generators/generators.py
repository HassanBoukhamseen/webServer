def response_generator(responses):
    while len(responses):
        http_response = responses.pop()
        yield http_response
        
def streaming_response_generator(response):
    status_line = f"{response.http_version} {response.status_code}\r\n"
    headers = "\r\n".join([f"{key}: {value}" for key, value in response.headers.items()])
    response_list = [status_line + headers + "\r\n\r\n"]
    response_list += response.body.split(" ")
    while len(response_list):
        chunk = response_list.pop(0)
        yield chunk + " "







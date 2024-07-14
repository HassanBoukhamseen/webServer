from webserver import WebServer
from test_text import text
from app.context_manager.context_manager import ServerContextManager

def main():
    port = 8081
    webserver = WebServer(port=port)
    assert WebServer(port=port) == webserver, f"{WebServer} is not a singleton class"

    @webserver.router.add('/sample_get', 'GET', needs_auth=False, streaming=True)
    def handle_get():
        return text

    @webserver.router.add('/needs_auth', 'GET', needs_auth=True, streaming=False)
    def needs_auth():
        return "This is a response for a request that needs authentication"

    @webserver.router.add('/sample_post', 'POST', needs_auth=False, streaming=False)
    def handle_post():
        return "This is a POST response"
    webserver.listen()

if __name__ == "__main__":
    main()


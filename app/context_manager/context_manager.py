class ServerContextManager:
    def __init__(self, webserver):
        self.webserver = webserver
    
    def __enter__(self):
        self.webserver.listen()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.webserver.close()


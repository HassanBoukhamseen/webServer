from app.router.router import Router
from app.listener.listener import Listener

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class WebServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.router = Router()
        self.port = port
        self.host = host
        self.listener = Listener(host=self.host, port=self.port, router=self.router)

    def listen(self):
        self.listener.listen()
    
    def close(self):
        self.listener.close()





    
    
    

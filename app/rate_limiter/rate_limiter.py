import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.clients = defaultdict(list)

    def is_allowed(self, client_id):
        current_time = time.time()
        request_times = self.clients[client_id]
        
        while request_times and request_times[0] <= current_time - self.time_window:
            request_times.pop(0)

        if len(request_times) < self.max_requests:
            request_times.append(current_time)
            return True
        else:
            return False



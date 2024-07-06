import time

class Logger:
    def __init__(self, log_file='./logs/logs.log'):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    def log_request(self, count, start_time, end_time, response, flag):
        elapsed_time = end_time - start_time
        log_message = f"Request {count}, elapsed time: {elapsed_time:.2f}s, request time: {start_time}, response flag: {flag}\n"
        self.log(log_message)

    def log_error(self, count, error):
        log_message = f"Request {count}, error: {str(error)}\n"
        self.log(log_message)
# -*- coding: utf-8 -*-
import requests
import time
import random
from datetime import datetime
import signal
import sys
import os
from config import headers, data, url

class Logger:
    """ 日志类 """
    def __init__(self, log_file):
        self.log_file = log_file

    def _write_log(self, log_message):
        """ 写日志 """
        with open(self.log_file, 'a') as f:
            f.write(log_message)

    def log_register(self, attempt_count, elapsed_time, response):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} [ REGISTER ] attempt {attempt_count}: Elapsed time: {elapsed_time:.2f}s, Response: {response}\n"
        self._write_log(log_message)

    def log_message(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} [ MESSAGE ] {message}\n"
        self._write_log(log_message)

    def log_exception(self, exception):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} [ EXCEPTION ] {str(exception)}\n"
        self._write_log(log_message)

    def log_error(self, attempt_count, error):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} [ ERROR ] attempt {attempt_count}: Error: {str(error)}\n"
        self._write_log(log_message)

class CourseRegistration:
    """ 抢课类 """
    def __init__(self):
        self.attempt_count = 0

    def _save_log(self, timestamp, log_message):
        """ 日志存储 """
        logs_dir = './logs/'
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, f'{timestamp}.log')
        with open(log_file, 'a') as f:
            f.write(log_message)

    def register_courses(self, min_time=1, max_time=3):
        """ 抢课 """
        print('Starting registration...')
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_log(timestamp, f"{current_time} [ MESSAGE ] starting registration\n")
        self.logger = Logger(os.path.join('./logs/', f'{timestamp}.log'))

        def signal_handler(sig, frame):
            print(f"Script aborted, signal: {signal.Signals(sig).name}")
            self.logger.log_exception(f"script aborted, signal: {signal.Signals(sig).name}")
            sys.exit(1)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        while True:
            self.attempt_count += 1
            try:
                start_time = time.time()
                response = requests.post(url, headers=headers, data=data)
                end_time = time.time()
                elapsed_time = end_time - start_time
                json_data = response.json()
                
                if 'flag' not in json_data:
                    print('Exception: Response missing "flag" parameter. Script terminated.')
                    self.logger.log_exception(f"miss 'flag' parameter in response, script terminated")
                    break
                
                flag = json_data.get('flag')

                if flag == '1':
                    self.logger.log_register(self.attempt_count, elapsed_time, "success")
                    break
                elif flag == '-1':
                    self.logger.log_register(self.attempt_count, elapsed_time, "fail")
                time.sleep(random.uniform(min_time, max_time)) # 随机 1-3s 间隔
            except Exception as e:
                print('Error occurred:', str(e))
                self.logger.log_error(self.attempt_count, e)
                break

if __name__ == "__main__":
    registration_instance = CourseRegistration()
    registration_instance.register_courses(min_time=1, max_time=2)
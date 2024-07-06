import requests
import time
import random
from config.config import headers, data
from logger.logger import Logger

def check_type(func):
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if not isinstance(arg, func.__annotations__[f'arg{i+1}']):
                raise TypeError(f"Argument {i+1} type error, should be {func.__annotations__[f'arg{i+1}']}")
        for key, value in kwargs.items():
            if not isinstance(value, func.__annotations__[key]):
                raise TypeError(f"Argument {key} type error, should be {func.__annotations__[key]}")
        return func(*args, **kwargs)
    return wrapper

@check_type
def pick_up(headers: dict, data: dict):
    url = 'http://newjw.hdu.edu.cn/jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512'
    logger = Logger()
    count = 0
    while True:
        count += 1
        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, data=data)
            end_time = time.time()
            json_data = response.json()
            flag = json_data.get('flag')

            if flag == '1':
                print('Stop sending requests')
                logger.log_request(count, start_time, end_time, response, flag)
                break
            elif flag == '-1':
                logger.log_request(count, start_time, end_time, response, flag)
            time.sleep(random.uniform(2, 3))
        except Exception as e:
            print('Error:', str(e))
            logger.log_error(count, e)
            break

def main():
    print("Start grabbing courses")
    pick_up(headers, data)

if __name__ == '__main__':
    main()
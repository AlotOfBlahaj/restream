import json
import logging
from functools import wraps
from os import mkdir
from os.path import abspath, dirname
from time import strftime, localtime, time, sleep

import requests
from retrying import retry

from config import sec_error, sec

ABSPATH = dirname(abspath(__file__))
fake_headers = {
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
}


@retry(wait_fixed=sec_error)
def get(url: str, mode='text'):
    try:
        r = requests.get(url, headers=fake_headers)
        if mode == 'img':
            return r
        else:
            return r.text
    except requests.RequestException:
        logger = get_logger('Requests')
        logger.exception('Network Error')


def get_json(url: str) -> dict:
    try:
        return json.loads(get(url))
    except json.decoder.JSONDecodeError:
        logger = get_logger('Json')
        logger.exception('Load Json Error')


def get_logger(module):
    logger = logging.getLogger(module)
    if not logger.handlers:
        logger.setLevel(level=logging.DEBUG)
        # 格式化
        formatter = logging.Formatter(
            f'%(asctime)s[%(levelname)s]: %(filename)s[line:%(lineno)d] - {module}: %(message)s')

        # 输出文件
        today = strftime('%m-%d', localtime(time()))
        try:
            file_handler = logging.FileHandler(f"log/log-{today}.log")
        except FileNotFoundError:
            mkdir('log')
            file_handler = logging.FileHandler(f"log/log-{today}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 输出流
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger


def while_warp(func):
    @wraps(func)
    def warp(*args, **kwargs):
        while True:
            func(*args, *kwargs)
            sleep(sec)

    return warp

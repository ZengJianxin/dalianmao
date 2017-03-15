from collections import OrderedDict
import re


class Router:

    def __init__(self):
        self.handlers = OrderedDict()

    def add(self, handler, url, method, params, data, json, extract_urls):
        url = re.compile(url)
        self.handlers[url] = {
            'method': method,
            'params': params,
            'data': data,
            'json': json,
            'extract_urls': extract_urls,
            'handler': handler
            }

    def remove(self, url):
        del self.handlers[re.compile(url)]

    def get(self, url):
        for key in self.handlers.keys():
            if key.fullmatch(url):
                return self.handlers[key]
        return None

    def check_url(self, url):
        for key in self.handlers.keys():
            if key.fullmatch(url):
                return True
        return False

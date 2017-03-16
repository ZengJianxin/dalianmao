from collections import OrderedDict
import re


class Router:

    def __init__(self):
        self.handlers = OrderedDict()

    def add(self, handler, url, json, extract_urls, js_source):
        url = re.compile(url)
        self.handlers[url] = {
            'json': json,
            'extract_urls': extract_urls,
            'handler': handler,
            'js_source': js_source,
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

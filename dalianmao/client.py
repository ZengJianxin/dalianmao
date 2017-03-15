import asyncio
from datetime import datetime
import os
import random
import time
import traceback
from urllib import parse

import aiofiles
from aiohttp import TCPConnector, ClientSession
from aiohttp.errors import ClientResponseError, TimeoutError
from bs4 import BeautifulSoup as bs

from dalianmao.exceptions import RetryError


class Client:

    def __init__(self, loop, options, router, logger):
        self.loop = loop
        self.options = options
        self.router = router
        self.logger = logger
        self.session = None
        self.proxies = []
        self.proxy_handler = None
        self.deny = [re.compile(deny) for deny in options.deny]

    def get_proxy(self):
        if self.proxy_handler:
            if len(self.proxies) == 0:
                proxies = self.proxy_handler()
                if len(proxies) > 0:
                    self.proxies = proxies
        if len(self.proxies) == 0:
            proxy = None
        else:
            proxy = random.choice(self.proxies)
        return proxy

    def del_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)

    async def get(self, url, referer=None):
        if not self.session:
            conn = TCPConnector(limit=self.options.concurrence, loop=self.loop)
            self.session = ClientSession(connector=conn, loop=self.loop, cookies=self.options.cookies)
        proxy = self.get_proxy()
        retry = 0
        while True:
            try:
                headers = self.options.headers
                if referer:
                    headers['Referer'] = referer
                time.sleep(random.random()*self.options.magic)
                resp = await self.session.get(
                    url = url,
                    headers = headers,
                    proxy = proxy,
                    proxy_auth = None,
                    allow_redirects = self.options.allow_redirects,
                    max_redirects = self.options.max_redirects,
                    timeout = self.options.timeout
                )
            except:
                retry += 1
                if retry > self.options.max_retry:
                    raise RetryError()
                if proxy:
                    self.del_proxy(proxy)
                else:
                    await asyncio.sleep(7200, loop=self.loop)
                continue
            else:
                return resp

    def is_denied(self, url):
        for rule in self.deny:
            if rule.fullmatch(url):
                return True
        return False

    def extract_urls(self, url, soup):
        urls = []
        for a in soup.find_all('a'):
            if a.has_attr('rel') and 'nofollow' in a['rel']:
                continue
            if a.has_attr('href'):
                href = a['href']
                if not href.startswith('http'):
                    href = parse.urljoin(url, href)
            urls.append(url)
        return urls

    def urls_filter(self, urls):
        for url in urls:
            if not self.router.check_url(url) or self.is_denied(url):
                urls.remove(url)
        return urls

    async def get_data(self, url, handlers):
        try:
            resp = await self.get(url)
        except RetryError:
            message = 'RetryError' + ' ' + 'Failed on requesting:' + ' ' + url
            await self.logger.warn(message)
            return [], handlers['handler'].__name__, None
        if resp.url != url:
            message = str(resp.status) + ' ' + url + ' redirected to ' + resp.url
            await self.logger.warn(message)
            handlers = self.router.get(resp.url)
            if not handlers:
                await resp.release()
                return [], None, None
        urls = []
        name = handlers['handler'].__name__
        data = None
        if resp.status // 100 == 2:
            try:
                if handlers['json']:
                    data = await resp.json()
                else:
                    content = await resp.text()
                    soup = bs(content, 'lxml')
                if not handlers['extract_urls']:
                    urls = self.extract_urls(resp.url, soup)
                else:
                    urls = handlers['extract_urls'](resp.url, soup)
                urls = self.urls_filter(urls)
                data = await handlers['handler'](resp.url, soup)
            except:
                message = 'Faild on parsing:' + ' ' + url + '\n' + traceback.format_exc()
                await self.logger.debug(message)
        else:
            message = str(resp.status) + ' ' +'Failed on requesting:' + ' ' + url
            await self.logger.warn(message)
        await resp.release()
        return urls, name, data

    async def download(self, url, path, filename, referer=None, mode='wb'):
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            resp = await self.get(url, referer=referer)
        except RetryError:
            message = 'RetryError' + ' ' + 'Faild on downloading:' + ' ' + url
            await self.logger.warn(message)
            return
        if resp.url != url or resp.status // 100 != 2:
            message = 'Faild on downloading:' + ' ' + url
            await self.logger.warn(message)
            await resp.release()
            return
        content = await resp.read()
        await resp.release()
        if not content:
            message = 'Faild on downloading:' + ' ' + url
            await self.logger.warn(message)
            return
        suffix = '.' + url.split('.')[-1]
        filepath = os.path.join(path, filename + suffix)
        if os.path.exists(filepath):
            now = datetime.now().strftime('-[%y-%m-%d %H:%M:%S]')
            filename = filename + now
            filepath = os.path.join(path, filename + suffix)
        f = await aiofiles.open(filepath, mode)
        await f.write(content)
        await f.close()
        return filename

    async def close(self):
        if self.session:
            await self.session.close()

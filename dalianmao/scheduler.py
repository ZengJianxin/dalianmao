import asyncio
from random import choice
from urllib import parse


class Scheduler:

    def __init__(self, loop):
        self.to_be_requested_q = asyncio.Queue(loop=loop)
        self.to_be_requested = []
        self.requesting = []
        self.requested = []

    async def put(self, urls):
        for url in urls:
            o = parse.urlparse(url)
            url = parse.urlunparse((o.scheme, o.netloc, o.path, '', '', ''))
            if url not in self.to_be_requested + self.requesting + self.requested:
                await self.to_be_requested_q.put(url)
                self.to_be_requested.append(url)

    def put_nowait(self, url):
        self.to_be_requested_q.put_nowait(url)
        self.to_be_requested.append(url)

    async def get(self):
        url = await self.to_be_requested_q.get()
        self.to_be_requested.remove(url)
        self.requesting.append(url)
        return url

    def release(self, url):
        self.requested.append(url)
        self.requesting.remove(url)
        self.to_be_requested_q.task_done()

    def is_finished(self):
        if len(self.requesting) + len(self.to_be_requested) > 0:
            return False
        return True

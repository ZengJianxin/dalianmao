import asyncio
from datetime import datetime
import os

from dalianmao.client import Client
from dalianmao.async_logging import Logger
from dalianmao.pipeline import Pipeline
from dalianmao.scheduler import Scheduler
from dalianmao.status import Status


class Engine:

    def __init__(self, loop, options, router):
        self.loop = loop
        self.options = options
        self.router = router
        self.scheduler = Scheduler(loop)
        self.status = Status(loop)
        self.logger = Logger(loop, options.filename, options.debug)
        self.client = Client(loop, options, router, self.logger)
        self.pipeline = Pipeline(loop, options.db, options.db_name, options.db_settings)

    def init(self, start_urls):
        for url in start_urls:
            self.scheduler.put_nowait(url)

    def resume(self):
        to_be_requested, = self.status.load_previous_status('to_be_requested')
        requesting, = self.status.load_previous_status('requesting')
        requested, = self.status.load_previous_status('requested')
        for url in to_be_requested + requesting:
            self.scheduler.put_nowait(url)
        self.scheduler.requested = requested
        to_be_requested, requesting, requested = None, None, None

    async def save_current_status(self):
        await self.status.save_current_status(to_be_requested=self.scheduler.to_be_requested)
        await self.status.save_current_status(requesting=self.scheduler.requesting)
        await self.status.save_current_status(requested=self.scheduler.requested)

    async def worker(self):
        while True:
            url = await self.scheduler.get()
            handlers = self.router.get(url)
            if handlers:
                urls, name, data = await self.client.get_data(url, handlers)
                await self.scheduler.put(urls)
                if data:
                    for datum in data:
                        await self.pipeline.save(name, datum)
                    await self.logger.info(url + ' ' + 'parsed')
            self.scheduler.release(url)
            if self.scheduler.is_finished():
                break

    async def close(self):
        await self.client.close()
        await self.pipeline.close()
        await self.save_current_status()
        message = 'Spider closed'
        await self.logger.info(message)
        await self.logger.close()

    async def _run(self):
        message = 'Spider opened'
        await self.logger.info(message)
        status = os.path.join(os.getcwd(), 'status')
        if len(os.listdir(status)) < 3:
            self.init(self.options.start_urls)
        else:
            self.resume()
        for _ in range(self.options.concurrence):
            self.loop.create_task(self.worker())
        while not self.scheduler.is_finished():
            await asyncio.sleep(30*60, loop=self.loop)
            await self.save_current_status()
        await self.close()

    def run(self):
        task = self.loop.create_task(self._run())
        self.loop.run_until_complete(task)
        self.loop.close()

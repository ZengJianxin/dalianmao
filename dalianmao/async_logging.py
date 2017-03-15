from datetime import datetime
import os

import aiofiles


class Logger:
    def __init__(self, loop, filename, debug):
        self.loop=loop
        self.filename = filename
        self._debug = debug
        self.logger = None

    async def log(self, prefix, message):
        message = prefix + '[' + datetime.now().strftime('%y-%m-%d %H:%M:%S') + ']' + '\t' + message + '\r\n'
        if self._debug:
            print(message)
        else:
            if not self.logger:
                filename = os.path.join(os.getcwd(), self.filename + '.log')
                self.logger = await aiofiles.open(filename, 'a', loop=self.loop)
            await self.logger.write(message)
            await self.logger.flush()

    async def info(self, message):
        prefix = '[INFO]'
        await self.log(prefix, message)

    async def debug(self, message):
        prefix = '[DEBUG]'
        await self.log(prefix, message)

    async def warn(self, message):
        prefix = '[WARN]'
        await self.log(prefix, message)

    async def error(self, message):
        prefix = '[ERROR]'
        await self.log(prefix, message)

    async def critical(self, message):
        prefix = '[CRITICAL]'
        await self.log(prefix, message)

    async def close(self):
        if self.logger:
            await self.logger.close()

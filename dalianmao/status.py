import json
import os

import aiofiles


class Status:

    def __init__(self, loop):
        self.loop = loop
        self.path = os.path.join(os.getcwd(), 'status')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    async def save_current_status(self, **kargs):
        for key in kargs:
            src = os.path.join(self.path, key)
            dst = os.path.join(self.path, key + '-old')
            if os.path.exists(dst):
                os.remove(dst)
            if os.path.exists(src):
                os.rename(src, dst)
            f = await aiofiles.open(src, 'w', loop=self.loop)
            await f.write('\n'.join(kargs[key]))
            await f.flush()
            await f.close()

    def load_previous_status(self, *args):
        status = []
        for value in args:
            src = os.path.join(self.path, value)
            old = os.path.join(self.path, value + '-old')
            if not os.path.exists(src):
                if os.path.exists(old):
                    src = old
                else:
                    raise FileNotFoundError()
            f = open(src, 'r')
            content = f.read()
            urls = [url for url in content.split('\n')]
            status.append(urls)
            f.close()
        return status

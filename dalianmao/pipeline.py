import asyncio

from motor.motor_asyncio import AsyncIOMotorClient as Motor


class Pipeline():
    def __init__(self, loop, db, db_name, db_settings):
        self.loop = loop
        self.db = db
        self.db_name = db_name
        self.db_settings = db_settings
        self.conn = None

    def connect_mongodb(self):
        client= Motor(**self.db_settings)
        self.conn = client[self.db_name]

    def connect_db(self):
        if self.db == 'mongodb':
            self.connect_mongodb()

    async def save_mongodb(self, name, data):
        await self.conn[name].insert_one(data)

    async def save(self, name, data):
        if not self.conn:
            self.connect_db()
        if not data:
            return
        if self.db == 'mongodb':
            await self.save_mongodb(name, data)

    async def close(self):
        pass

import os

from peewee import *

database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Database:

    def __init__(self, output):
        database_dir = os.path.join(output, 'mutation.db')
        self.db = SqliteDatabase(database_dir)
        database_proxy.initialize(self.db)

from peewee import *

database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Database:

    def __init__(self, database_dir):
        self.db = SqliteDatabase(database_dir)
        database_proxy.initialize(self.db)

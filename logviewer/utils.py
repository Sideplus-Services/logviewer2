import re

from dotenv import dotenv_values
from pymongo import MongoClient

RE_MONGODB = re.compile("MONGO_URI_(.*)")


class DB:
    def __init__(self):
        self.envfile = dotenv_values(".env")
        self.dbs = dict()
        self.dbs_conns = dict()

        for (key, value) in self.envfile.items():
            match = re.match(RE_MONGODB, key)
            if match:
                self.dbs[int(match.groups()[0])] = value

        for (gid, connURI) in self.dbs.items():
            self.dbs_conns[gid] = MongoClient(connURI).modmail_bot

    def get(self, gid):
        return self.dbs_conns.get(int(gid), None)

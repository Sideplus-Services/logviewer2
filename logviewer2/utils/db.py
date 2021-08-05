from dotenv import dotenv_values
from pymongo import MongoClient
from logviewer2.utils.regexcfg import GET_MCONFIG


class DB:
    def __init__(self):
        self.envfile = dotenv_values(".env")
        self.dbs = GET_MCONFIG(self.envfile)
        self.dbs_conns = dict()

        for (gid, connURI) in self.dbs.items():
            self.dbs_conns[gid] = MongoClient(connURI).modmail_bot

    def get(self, gid):
        return self.dbs_conns.get(int(gid), None)

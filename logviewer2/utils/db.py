import os

from pymongo import MongoClient

from logviewer2.utils import GET_INSTANCE
from logviewer2.utils.regexcfg import GET_MCONFIG


class DB:
    def __init__(self):
        self.dbs = GET_MCONFIG(os.environ)
        self.dbs_conns = dict()

        for (gid, connURI) in self.dbs.items():
            gid, instance = GET_INSTANCE(gid)
            if gid not in self.dbs_conns:
                self.dbs_conns[gid] = dict()
            self.dbs_conns[gid].update({instance: MongoClient(connURI).modmail_bot})

    def get(self, gid, instance_id):
        ginstances = self.dbs_conns.get(gid, dict())
        return ginstances.get(instance_id, None)

import json
from pymongo import ASCENDING, DESCENDING
from bson import json_util


class MongoHandler(object):
    SORT_TAG = {-1: DESCENDING, 1: ASCENDING}

    def __init__(self, conn):
        self.mongoConn = conn

    def get_dbname_in_uri(self):
        try:
            return self.mongoConn.get_default_database().name
        except:
            pass
        return None

    @staticmethod
    def _bson2json(s):
        return None if s is None else json.loads(s, object_hook=json_util.object_hook)

    def cmd_status(self, db, col, args):
        return {"status": self.mongoConn[db].command("collstats", col)}

    def cmd_count(self, db, col, args):
        criteria = self._bson2json(args.get("criteria", "{}"))
        return {"count": self.mongoConn[db][col].find(criteria).count()}

    def cmd_find(self, db, col, args):
        if "limit" not in args:
             return {"error":"Parameter Error"}
        criteria = self._bson2json(args.get("criteria", "{}"))
        fields = self._bson2json(args.get("fields", None))
        limit = int(args.get("limit", "0"))
        if limit > 100:
             return {"error":"Parameter Error"}
        skip = int(args.get("skip", "0"))
        # batchsize = int(args.get("batch_size", "15"))

        cursor = self.mongoConn[db][col].find(criteria, fields, limit=limit, skip=skip)

        sort = self._bson2json(args.get("sort", "{}"))
        if sort:
            pymongoSort = [(k, MongoHandler.SORT_TAG.get(v, ASCENDING)) for k, v in sort.items()]
            cursor.sort(pymongoSort)
        return {"results": list(cursor)}

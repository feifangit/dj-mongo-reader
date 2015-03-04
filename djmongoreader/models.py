from django.conf import settings
from pymongo import MongoClient, MongoReplicaSetClient
from .mongoreader import MongoHandler

_MONGO_CONN_STR = settings.MONGO_READER_SETTINGS.get("conn_str")

_conn = MongoClient(_MONGO_CONN_STR)
if _conn._MongoClient__repl:
    _conn = MongoReplicaSetClient(_MONGO_CONN_STR)


mongoReader = MongoHandler(_conn)

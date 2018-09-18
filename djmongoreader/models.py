from django.conf import settings
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference
from .mongoreader import MongoHandler

_MONGO_CONN_STR = settings.MONGO_READER_SETTINGS.get("conn_str")

_conn = MongoClient(_MONGO_CONN_STR)
try:  # to support pymongo 2.x
	if settings.MONGO_READER_SETTINGS.get("replicaset"):
	    _conn = MongoReplicaSetClient(_MONGO_CONN_STR, replicaSet=settings.MONGO_READER_SETTINGS.get("replicaset"), ReadPreference = ReadPreference.PRIMARY_PREFERRED)
except:
	pass

mongoReader = MongoHandler(_conn)
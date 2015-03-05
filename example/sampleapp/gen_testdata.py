import datetime
from pymongo import MongoClient as MC
col = MC().db1.user_collection1

day = datetime.datetime.now()

for i in range(100):
	day -= datetime.timedelta(days=30)
	col.insert({'name':'user %s' % i, 
		'gender': 0 if i%2 else 1,
		'disable': True if i%3 else False, 
		'lastlogin': day})

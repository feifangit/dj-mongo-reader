====
dj-mongo-reader
====

dj-mongo-reader is a Django application can be used to query MongoDB via AJAX requests and render result with several customization options.


Installation
--------
- (TODO) Install from PyPi ``pip install dj-mongo-reader`` 
- Install from source code

	1. download code ``git clone https://github.com/feifangit/dj-mongo-reader.git``
 	2. run ``<setup.py>`` from ``dj-mongo-reader`` folder ``python setup.py install``


Features
--------
1. Able to send ``find``, ``count``, ``collstats`` commands to MongoDB via designated URL
2. Basic HTML pages included, only few code is needed to **work with your existing CSS framework**
3. **Pagination** implemented, you can customize record number show in each page
4. **Permission check**, you can deny a data fetching request based on user's permission and the query(database, collection, command, criteria).
5. Pick up some keys of the record to fill the table, leave complete record in **detail dialog**
6. Assign **display names** for keys in MongoDB record
7. **value transformation**, you can provide Javascript callback functions to process raw value data from MongoDB to a proper text for displaying



DEMO
--------
A Django application runs on heroku.

 - Functionality: A query form and result table included.
 - UI: Bootstrap 3 applied.

| URL: http://dj-mongo-reader.herokuapp.com
| `Source code </example/>`_


Quick start
--------
1. add **dj-mongo-reader** to ``INSTALLED_APPS`` in ``<settings.py>``

2. add JSON-type variable **MONGO_READER_SETTINGS** in ``<settings.py>``
 - **conn_str**, MongoDB connection string, see http://docs.mongodb.org/manual/reference/connection-string/
 - **perm_check_func**, a string represent path to a permission verification function
 
 e.g. ::

		MONGO_READER_SETTINGS = {
		    "conn_str": "mongodb://10.1.5.10:27017/2",
		    "perm_check_func": "somewhere.security.my_mongocall_perm_check",

		}
 
 in file ``<somewhere/security.py>``, we have the permission verification ready ::

		def my_mongocall_perm_check(req, db, col, cmd):
			u = req.user
			if (not u) or (not u.is_authenticated()):
			    return False
			
			if db != "dbforapp1":  # limit db to dbforapp1
			    return False
			
			if not col.startswith("transaction_"):  # limit collection to transaction_.*
			    return False
			
			q = json.loads(req.GET.get("criteria", "{}"))  # limit parameter based on criteria
			if u.company and u.company.id != int(q.get("company", "-1")):
			    return False
			return True

3. URL dispatch

add url route to your ``<urls.py>`` ::

 	urlpatterns = patterns('',
	 	...
		url(r'^mongo/', include('dj-mongo-reader.urls'))
		...

4. embed into your own HTML

parameters for ``dj-mongo-reader/table.html``

 - db
 - col
 - cmd
 - rowcount (optional), default 50
 - criteria, JSON format 
 - sort, JSON format
 - columns, string, key names connected by comma
 - columns_trans (optional), JSON format, a database key name to display name mapping.


5. customize your result page
create folder ``dj-mongo-reader`` under your ``templates`` folder





Credits
--------
| Fan Fei feifan.pub@gmail.com backend
| Neil Chen neil.chen.nj@gmail.com frontend 

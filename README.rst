dj-mongo-reader
===============
dj-mongo-reader is a Django application can be used to query MongoDB via AJAX requests and render result with several customization options.

Installation
------------
- Install from PyPi ``pip install dj-mongo-reader`` 
- Install from source code

 - download code ``git clone https://github.com/tofu0913/dj-mongo-reader.git``
 - run ``<setup.py>`` from ``dj-mongo-reader`` folder ``python setup.py install``

Features
--------
1. Able to send ``find``, ``count``, ``collstats`` commands to MongoDB via designated URL
2. Basic HTML pages included, only few code is needed to **work with your existing CSS framework**
3. **Pagination** implemented, you can customize record number show in each page
4. **Permission check**, you can deny a data fetching request based on user's permission and the query(database, collection, command, criteria).
5. Pick up some keys of the record to fill the table, leave complete record in **detail dialog**
6. Assign **display names** for keys in MongoDB record
7. **value transformation**, you can provide Javascript callback functions to process raw value data from MongoDB to a proper text for displaying
8. export MongoDB data to CSV file (use it carefully for larage amount of records)

DEMO and Document
------------------
A Django application runs on heroku.

- Functionality: A query form and result table included.
- UI: Bootstrap 3 applied.

| URL: http://dj-mongo-reader.herokuapp.com
| Source code Please see ``example`` folder


Guide
------------
http://dj-mongo-reader.herokuapp.com





Credits
--------

- Fan Fei feifan.pub@gmail.com backend
- Neil Chen neil.chen.nj@gmail.com frontend 
- Cliff Chen tofu0913@gmail.com fork and maintenance 

import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from djmongoreader.models import mongoReader


def readme(request):
    context = {"githubraw": "https://raw.githubusercontent.com/feifangit/dj-mongo-reader/master/example/sampleapp",
            "githuburl": "https://github.com/feifangit/dj-mongo-reader/blob/master/example/sampleapp"}
    return render_to_response("readme.html", context)


def query(request):
    _dbname = mongoReader.get_dbname_in_uri()
    dbname = _dbname if _dbname else "db1"
    context = {"db": dbname,
            "col": "user_collection1",
            "rowcount": 10,
            "sort": json.dumps({"name": -1}),
            "columns": "name,disable,gender,lastlogin",
            "columns_trans": json.dumps({"name": "user name", "lastlogin": "last login"})
    }
    return render_to_response("query.html", context)

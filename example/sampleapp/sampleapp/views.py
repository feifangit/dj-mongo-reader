import json
from django.shortcuts import render_to_response
from django.template import RequestContext


def readme(request):
    context = RequestContext(request)
    args = {}
    return render_to_response("readme.html", args, context_instance=context)


def query(request):
    context = RequestContext(request)
    args = {"db": "db1",
            "col": "user_collection1",
            "rowcount": 10,
            "sort": json.dumps({"name": -1}),
            "columns": "name,disable,gender,lastlogin",
            "columns_trans": json.dumps({"name": "user name", "lastlogin": "last login"})
    }
    return render_to_response("query.html", args, context_instance=context)

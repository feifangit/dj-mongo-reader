import logging
import traceback
import time
import csv
from bson import json_util
from pymongo import ASCENDING
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from .utility import jsonify, perm_check, EnhancedDictWriter
from .models import mongoReader

logger = logging.getLogger('djmongoreader')


@jsonify
def blank(request, *args, **kwargs):
    return {}


@jsonify
def info(request):
    return {"client_clz": str(type(mongoReader.mongoConn))}


@jsonify(options={"default": json_util.default})
@perm_check
def restcall(request, db, col, cmd):
    logger.debug("rest call %s %s %s", db, col, cmd)
    if not hasattr(mongoReader, "cmd_%s" % cmd):
        return {"error": "no command found", "ok": 0}

    try:
        st = time.time()
        r = getattr(mongoReader, "cmd_%s" % cmd)(db, col, request.GET)
        r["ok"] = 1
        r["span"] = time.time() - st
        return r
    except Exception as e:
        traceback.print_exc()
        return {"ok": 0, "error": str(e)}


class Echo(object):  # a file-alike class to hook csv outputting
    def write(self, value):
        return value


@perm_check
def exportcsv(request, db, col, cmd):
    args = request.GET
    criteria = mongoReader._bson2json(args.get("criteria", "{}"))
    fields = mongoReader._bson2json(args.get("projection", "{}"))
    exportfilename = args.get("exportfn", "export.csv")

    if not fields:
        return HttpResponse("parameter fields must be specified")

    find_projection = dict(zip(fields.keys(),[1]*len(fields)))
    if "_id" not in fields:  # dismiss _id explicitly 
        find_projection["_id"] = 0
    
    cursor = mongoReader.mongoConn[db][col].find(criteria, find_projection)

    sort = mongoReader._bson2json(args.get("sort", "{}"))
    if sort:
        pymongoSort = [(k, mongoReader.SORT_TAG.get(v, ASCENDING))
                       for k, v in sort.items()]
        cursor.sort(pymongoSort)

    pseudo_buffer = Echo()
    writer = EnhancedDictWriter(pseudo_buffer, fields)

    def stream():
        yield writer.writerow(fields)
        for row in cursor:
            yield writer.writerow(row)

    response = StreamingHttpResponse(stream(), content_type="text/csv")

    response['Content-Disposition'] = 'attachment; filename="%s"' % exportfilename
    return response

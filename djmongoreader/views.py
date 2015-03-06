import logging
import traceback
import time
from bson import json_util

from django.conf import settings
from .utility import jsonify, perm_check
from .models import mongoReader


logger = logging.getLogger('djmongoreader')


@jsonify
def blank(request, *args, **kwargs):
    return {}


@jsonify
def info(request):
    return {"client_clz": str(type(mongoReader.mongoConn)) }


@jsonify(options={"default": json_util.default})
@perm_check
def restcall(request, db, col, cmd):
    logger.debug("rest call %s %s %s", db, col, cmd)
    if hasattr(mongoReader, "cmd%s" % cmd):
        try:
            st = time.time()
            r = getattr(mongoReader, "cmd%s" % cmd)(db, col, request.GET)
            r["ok"] = 1
            r["span"] = time.time() - st
            return r
        except Exception as e:
            traceback.print_exc()
            return {"ok": 0, "error": str(e)}
    return {"error": "no command found", "ok": 0}

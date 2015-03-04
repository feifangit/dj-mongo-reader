import json

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils.module_loading import import_by_path

_perm_check_func_name = settings.MONGO_READER_SETTINGS.get("perm_check_func")
_perm_check_func = import_by_path(_perm_check_func_name) if _perm_check_func_name else None


def jsonify(function=None, options={}):
    def real_decorator(func):
        def wrapped(*args, **kwargs):
            resp = HttpResponse(json.dumps(func(*args, **kwargs), **options))
            resp["Content-Type"] = "application/json"
            return resp
        return wrapped
    return real_decorator if not function else real_decorator(function)


def perm_check(function, perm_check_func=_perm_check_func, raise_exception=False):
    """
    perm_check_func: the auth func with parameter db,col,cmd
    raise_exception: True: raise http 403 exception if permission check failed, otherwise return a JSON
    """
    def real_decorator(func):
        def wrapped(request, db, col, cmd, *args, **kwargs):
            bPermPass = perm_check_func(request, db, col, cmd) if perm_check_func else True
            if raise_exception and (not bPermPass):
                raise PermissionDenied
            return func(request, db, col, cmd, *args, **kwargs) if bPermPass else {"error": "permission disallowed"}

        return wrapped
    return real_decorator(function)

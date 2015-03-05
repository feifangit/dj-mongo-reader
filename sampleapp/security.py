import json


def my_mongocall_perm_check(req, db, col, cmd):
    # u = req.user

    if db != "dbforapp1":  # limit db to dbforapp1
        return False

    if not col.startswith("transaction_"):  # limit collection to transaction_.*
        return False

    q = json.loads(req.GET.get("criteria", "{}"))  # limit parameter based on criteria
    # todo limit q
    return True

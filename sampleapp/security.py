import json


def my_mongocall_perm_check(req, db, col, cmd):
    if db != "db1":  # limit db to db1
        return False

    if not col.startswith("user"):  # limit collection to transaction_.*
        return False

    return True

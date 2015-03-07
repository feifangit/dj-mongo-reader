
def my_mongocall_perm_check(req, db, col, cmd):
    if not col.startswith("user"):  # limit collection to transaction_.*
        return False

    return True

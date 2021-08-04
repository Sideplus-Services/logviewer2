from functools import wraps

from flask import current_app, abort


def with_logs(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        gid = kwargs['gid']
        logkey = kwargs['logkey']
        db = current_app.db.get(gid)
        if not db:
            abort(404)

        document = db.logs.find_one({"key": logkey})
        if not document:
            abort(404)
        return fn(document, *args, **kwargs)
    return decorated_view

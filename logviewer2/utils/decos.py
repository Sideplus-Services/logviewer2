from functools import wraps

from flask import current_app, abort, g, session, request, url_for, redirect


def with_logs(fn):
    @wraps(fn)
    def decorated_view(user=None, *args, **kwargs):
        gid = kwargs['gid']
        logkey = kwargs['logkey']
        db = current_app.db.get(gid)
        if not db:
            abort(404)

        # Force auth TODO: MAKE THIS WORK FOR REAL :)
        oauth_enabled = True
        if oauth_enabled:
            # check user id (pass check
            if not current_app.discord.authorized:
                session["next_url"] = request.path
                return redirect(url_for("auth.auth_discord"))
            current_user = current_app.discord.fetch_user()
            if current_user != current_user:  # fake auth
                abort(403)

        document = db.logs.find_one({"key": logkey})
        if not document:
            abort(404)
        return fn(document, user, *args, **kwargs)

    return decorated_view


def authed(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if not current_app.discord.authorized:
            abort(403)
        return func(*args, **kwargs)

    return deco


def authed_redirect(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if not current_app.discord.authorized:
            session["next_url"] = request.path
            return redirect(url_for("auth.auth_discord"))
        return func(*args, **kwargs)

    return deco


def with_user(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if current_app.discord.authorized:
            user = current_app.discord.fetch_user()
        else:
            user = {}
        return func(user, *args, **kwargs)

    return deco

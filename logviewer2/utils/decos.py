from functools import wraps

from flask import current_app, abort, g, session, request, url_for, redirect
from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from flask_discord import Unauthorized

from logviewer2.log_utils.models import LogEntry


def with_logs(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        gid = kwargs['gid']
        logkey = kwargs['logkey']
        db = current_app.db.get(gid)
        if not db:
            abort(404)

        # get plugin config if exists
        plconfig = db.plugins.logviewer2companion.find_one({"_id": "config"}) or {}

        if plconfig.get("enabled", False):
            if not current_app.discord.authorized:
                session["next_url"] = request.path
                return redirect(url_for("auth.auth_discord"))
            current_user = current_app.discord.fetch_user()
            if current_user.id not in plconfig.get("allowed_users", []):
                abort(403)

        document = db.logs.find_one({"key": logkey})
        if not document:
            abort(404)
        g.document = LogEntry(document)
        return fn(*args, **kwargs)

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
            try:
                user = current_app.discord.fetch_user()
            except InvalidClientError:
                current_app.discord.revoke()
                session["next_url"] = request.path
                return redirect(url_for("auth.auth_discord"))
        else:
            user = None
        g.user = user
        return func(*args, **kwargs)

    return deco

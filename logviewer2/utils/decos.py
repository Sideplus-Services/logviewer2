from functools import wraps

from flask import current_app, abort, g, session, request, url_for, redirect
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError

from logviewer2.log_utils.models import LogEntry
from logviewer2.utils import GET_INSTANCE


def with_logs_evidence(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        gid, instid = None, None
        try:
            gid, instid = GET_INSTANCE(kwargs['qid'])
        except ValueError:
            abort(404)

        logkey = kwargs['logkey']
        db = current_app.db.get(gid, instid)
        if db is None:
            abort(404)

        plconfig = db.plugins.Logviewer2Companion.find_one({"_id": "config"}) or {}

        if not plconfig.get("allow_evidence_share", False):
            # if its not enabled or no plugin config
            abort(403)

        document = db.logs.find_one({"key": logkey})
        if not document:
            abort(404)
        g.document = LogEntry(document, evidence=True)
        g.document.internal_messages = []  # :) remove internal messages from class
        return fn(*args, **kwargs)

    return decorated_view


def with_logs(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        gid, instid = None, None
        try:
            gid, instid = GET_INSTANCE(kwargs['qid'])
        except ValueError:
            abort(404)

        logkey = kwargs['logkey']

        db = current_app.db.get(gid, instid)
        if db is None:
            abort(404)

        # get plugin config if exists
        plconfig = db.plugins.Logviewer2Companion.find_one({"_id": "config"}) or {}

        if plconfig.get("enabled", False):
            if not current_app.discord.authorized:
                session["next_url"] = request.path
                return redirect(url_for("auth.auth_discord"))

            try:
                current_user = current_app.discord.fetch_user()
            except (InvalidClientError, TokenExpiredError):
                return redirect(url_for("auth.auth_discord"))

            allowed_users = []
            for role in plconfig.get("allowed_roles", {}):
                allowed_users += plconfig.get("allowed_roles", {})[role]
            allowed_users += plconfig.get("allowed_users", [])

            if current_user.id not in allowed_users:
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


def with_user(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if current_app.discord.authorized:
            try:
                user = current_app.discord.fetch_user()
            except (InvalidClientError, TokenExpiredError):
                return redirect(url_for("auth.auth_discord"))
        else:
            user = None
        g.user = user
        return func(*args, **kwargs)

    return deco

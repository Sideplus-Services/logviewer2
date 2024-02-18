from flask import Blueprint, current_app, redirect, session, url_for
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError, MismatchingStateError

from logviewer2.utils.decos import authed

Auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@Auth.route('/logout', methods=["GET", "POST"])
@authed
def auth_discord_logout():
    current_app.discord.revoke()
    return redirect(url_for("root"))


@Auth.get('/discord')
def auth_discord():
    return current_app.discord.create_session(
        scope=["identify", "email", "guilds", "guilds.members.read", "connections"], prompt=False)


@Auth.get('/discord/callback')
def auth_discord_callback():
    try:
        current_app.discord.callback()
    except MismatchingStateError:
        return redirect(url_for("auth.auth_discord"))

    if session.get("next_url", None):
        url = str(session["next_url"])
        del session["next_url"]
        return redirect(url)
    return redirect(url_for("root"))


@Auth.get('/@me')
@authed
def auth_me():
    try:
        data = dict(current_app.discord.fetch_user().__dict__)
    except (InvalidClientError, TokenExpiredError):
        return redirect(url_for("auth.auth_discord"))
    for k in list(data.keys()):
        if k.startswith('_'):
            del data[k]
    return data

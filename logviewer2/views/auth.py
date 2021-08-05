from flask import Blueprint, current_app, redirect, session

from logviewer2.utils.decos import authed, authed_redirect

Auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@Auth.route('/logout', methods=['POST', 'GET'])
@authed
def auth_discord_logout():
    current_app.discord.revoke()
    return redirect("/")


@Auth.route('/discord')
def auth_discord():
    return current_app.discord.create_session(scopes=["identify"], prompt=False)


@Auth.route('/discord/callback')
def auth_discord_callback():
    current_app.discord.callback()
    if session.get("next_url", None):
        url = str(session["next_url"])
        del session["next_url"]
        return redirect(url)
    return redirect("/")


@Auth.route('/@me')
@authed_redirect
def auth_me():
    # clean data :)
    data = dict(current_app.discord.fetch_user().__dict__)
    for k in list(data.keys()):
        if k.startswith('_'):
            del data[k]
    return data

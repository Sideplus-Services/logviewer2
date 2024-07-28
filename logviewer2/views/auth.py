from flask import Blueprint, current_app, redirect, session, url_for
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError, MismatchingStateError

from logviewer2.utils.decos import authed

Auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@Auth.route('/logout', methods=["GET", "POST"])
@authed
def auth_discord_logout():
    current_app.discord.revoke()
    session.clear()  # Clear the session on logout
    return redirect(url_for("root"))


@Auth.get('/discord')
def auth_discord():
    # Store the next URL in the session if provided
    next_url = request.args.get('next', None)
    if next_url:
        session['next_url'] = next_url
    return current_app.discord.create_session(
        scope=["identify", "email", "guilds", "guilds.members.read", "connections"], prompt=False)


@Auth.get('/discord/callback')
def auth_discord_callback():
    try:
        # Handle the OAuth2 callback and fetch the token
        token = current_app.discord.callback()
        session['oauth_token'] = token
    except MismatchingStateError:
        # Redirect to login if the state doesn't match
        return redirect(url_for("auth.auth_discord"))
    except InvalidClientError as e:
        # Handle client errors
        print(f"Invalid client error: {e}")
        return redirect(url_for("auth.auth_discord"))
    except TokenExpiredError as e:
        # Handle expired tokens
        print(f"Token expired error: {e}")
        return redirect(url_for("auth.auth_discord"))

    # Redirect to the next URL if provided
    if 'next_url' in session:
        url = session.pop('next_url')
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

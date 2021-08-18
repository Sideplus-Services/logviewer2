from dotenv import dotenv_values
from flask import Flask, render_template, Response, g
from flask_discord import DiscordOAuth2Session
from logviewer2.utils.decos import with_logs, with_user
from logviewer2.utils.db import DB
from logviewer2.utils.regexcfg import GET_DCONFIG
from logviewer2.views import Auth

config = dotenv_values(".env")
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object(__name__)
app.config.update(
    SECRET_KEY=bytes(config.get("FLASK_SECRET_KEY"), 'utf8'),
    MAX_CONTENT_LENGTH=(16 * 1024 * 1024)
)

app.db = DB()
# Auth :)
dconfig = GET_DCONFIG(config)
DiscordOAuth2Session(app, client_id=dconfig["CLIENT_ID"], client_secret=dconfig["CLIENT_SECRET"],
                     redirect_uri=dconfig["CLIENT_REDIRECT_URI"])
app.register_blueprint(Auth)


# errors
@app.errorhandler(403)
@with_user
def page_not_found(e):
    return render_template("unauthorized.html", user=g.user), 403


@app.errorhandler(404)
@with_user
def page_not_found(e):
    return render_template("not_found.html", user=g.user), 404


@app.errorhandler(500)
@with_user
def page_not_found(e):
    return render_template("server_error.html", user=g.user), 500


# Pages
@app.route("/")
@with_user
def root():
    return render_template('index.html', user=g.user)


@app.route("/robots.txt")
def robotstxt():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.route("/<int:gid>/<logkey>")
@with_user
def logviewer_render(gid, logkey):
    return g.document.render_html(user=g.user)


# API killme
@app.route("/api/raw/<int:gid>/<logkey>")
@with_logs
def api_raw_render(gid, logkey):
    return Response(g.document.render_plain_text(), mimetype="text/plain"), 200

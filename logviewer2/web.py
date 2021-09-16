import os
import signal

from dotenv import dotenv_values
from flask import Flask, render_template, Response, g
from flask_discord import DiscordOAuth2Session

from werkzeug.middleware.proxy_fix import ProxyFix

from logviewer2.utils import GET_SECRET_KEY, DOWNLOAD_FONTS
from logviewer2.utils.decos import with_logs_evidence, with_logs, with_user
from logviewer2.utils.db import DB
from logviewer2.utils.regexcfg import GET_DCONFIG
from logviewer2.views import Auth, Fproxy

config = dotenv_values(".env")
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(__name__)
app.config.update(
    SECRET_KEY=GET_SECRET_KEY(config),
    MAX_CONTENT_LENGTH=(16 * 1024 * 1024),
    FDIR=DOWNLOAD_FONTS(),
    ISSHUTDOWN=False
)


def keyboardInterruptHandler(s, frame):
    if not app.config['ISSHUTDOWN']:
        app.config['ISSHUTDOWN'] = True
        if app.config.get("FDIR", False):
            print("cleaning up Fonts")
            app.config["FDIR"].cleanup()
        os.kill(os.getpid(), signal.SIGTERM)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

app.db = DB()
# Auth :)
dconfig = GET_DCONFIG(config)
DiscordOAuth2Session(app, client_id=dconfig["CLIENT_ID"], client_secret=dconfig["CLIENT_SECRET"],
                     redirect_uri=dconfig["CLIENT_REDIRECT_URI"])
app.register_blueprint(Auth)
app.register_blueprint(Fproxy)


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
@with_logs
def logviewer_render(gid, logkey):
    return g.document.render_html(user=g.user)


@app.route("/evidence/<int:gid>/<logkey>")
@with_user
@with_logs_evidence
def logviewer_render_evidence(gid, logkey):
    return g.document.render_html(user=g.user)


# API killme
@app.route("/api/raw/<int:gid>/<logkey>")
@with_logs
def api_raw_render(gid, logkey):
    return Response(g.document.render_plain_text(), mimetype="text/plain"), 200

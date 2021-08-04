from flask import Flask, render_template, abort, Response

from logviewer.decos import with_logs
from logviewer.log_utils.models import LogEntry
from logviewer.utils import DB

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object(__name__)
app.db = DB()


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("server_error.html"), 500


# Pages
@app.route("/")
def root():
    return render_template('index.html')


@app.route("/<gid>/<logkey>")
@with_logs
def logviewer_render(document, gid, logkey):
    return LogEntry(document).render_html()


# API killme
@app.route("/api/raw/<gid>/<logkey>")
@with_logs
def api_raw_render(document, gid, logkey):
    return Response(LogEntry(document).render_plain_text(), mimetype="text/plain"), 200

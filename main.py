from gevent import monkey # noqa
monkey.patch_all() # noqa
import psycogreen.gevent # noqa
psycogreen.gevent.patch_psycopg() # noqa

# Needs to be above to patch for gevent
from logging.config import dictConfig
from logviewer2.constants import Constants

import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import click
import dotenv
from werkzeug.serving import run_simple
dotenv.load_dotenv()


@click.group()
def cli():
    dictConfig({
        'version': 1,
        'formatters': {'default': {'format': Constants.LOG_FORMAT}},
        'handlers': {'wsgi': {'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout', 'formatter': 'default'}},
        'root': {'level': 'INFO', 'handlers': ['wsgi']}
    })


@cli.command()
def serve():
    from logviewer2.web import app

    app.debug = True
    return run_simple(os.environ.get("HOST", "localhost"), int(os.environ.get("PORT", "5214")), app, use_debugger=True,
                      use_reloader=True, use_evalex=True, threaded=True)
    # options = {
    #     "bind": f"{os.environ.get('HOST', 'localhost')}:{os.environ.get('PORT', '5214')}",
    #     "workers": 1,
    #     "worker_class": "gunicorn.workers.ggevent.GeventPyWSGIWorker",
    # }
    # return StandaloneApplication(app, options).run()


@cli.command()
@click.option('--new/--no-new', '-n', default=False)
def secretkey(new):
    from logviewer2.utils import GET_SECRET_KEY
    key = GET_SECRET_KEY({} if new else os.environ)
    if not new:
        print(key.decode("utf-8"))
    return key if not new else ""


if __name__ == '__main__':
    cli()

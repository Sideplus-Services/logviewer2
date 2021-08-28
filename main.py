from gevent import monkey;monkey.patch_all()

import sentry_sdk

from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

from logviewer2.utils import GET_REV

from logging.config import dictConfig
from logviewer2.constants import Constants


import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import click
from dotenv import dotenv_values
from werkzeug.serving import run_simple
from logviewer2.web import app
config = dotenv_values(".env")


@click.group()
def cli():
    dictConfig({
        'version': 1,
        'formatters': {'default': {'format': Constants.LOG_FORMAT}},
        'handlers': {'wsgi': {'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout', 'formatter': 'default'}},
        'root': {'level': 'INFO', 'handlers': ['wsgi']}
    })


@cli.command()
@click.option('--debug/--no-debug', '-d', default=True)
def serve(debug):
    sentry_sdk.init(
        dsn=config.get("SENTRY_DSN", None),
        release=GET_REV(),
        integrations=[FlaskIntegration(), ExcepthookIntegration(always_run=True)],
        traces_sample_rate=1.0
    )

    if debug:
        app.debug = True
        return run_simple(config.get("HOST", "localhost"), int(config.get("PORT", "5214")), app, use_debugger=True, use_reloader=True, use_evalex=True, threaded=True)
    else:
        return run_simple(config.get("HOST", "localhost"), int(config.get("PORT", "5214")), app, threaded=True)


if __name__ == '__main__':
    cli()

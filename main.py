from gevent import monkey

monkey.patch_all()

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import click
from dotenv import dotenv_values
from werkzeug.serving import run_simple
from logviewer2.web import app
config = dotenv_values(".env")


@click.group()
def cli():
    pass


@cli.command()
@click.option('--debug/--no-debug', '-d', default=True)
def serve(debug):
    if debug:
        app.debug = True
        return run_simple(config.get("HOST", "localhost"), int(config.get("PORT", "5214")), app, use_debugger=True, use_reloader=True, use_evalex=True, threaded=True)
    else:
        return run_simple(config.get("HOST", "localhost"), int(config.get("PORT", "5214")), app, threaded=True)


if __name__ == '__main__':
    cli()

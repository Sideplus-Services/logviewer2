import sys
import subprocess

scripts = {
    # NOTE: should add -k gevent, but it doesn't work? "ReferenceError: weakly-referenced object no longer exists"
    "web": "python -m gunicorn logviewer2.web:app --preload --workers 3 --access-logfile -",
    "webd": "python main.py serve",
    "secret": "python main.py secretkey",
    "gensecret": "python main.py secretkey --new"
}


def __getattr__(name):
    cmd = scripts.get(name, None)
    if not cmd:
        raise Exception("No script found")

    subprocess.run(cmd.split(" ") + sys.argv[1:])
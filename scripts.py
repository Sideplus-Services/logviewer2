import sys
import subprocess

scripts = {
    "web": "python main.py serve --no-debug",
    "webd": "python main.py serve --debug",
    "secret": "python main.py secretkey",
    "gensecret": "python main.py secretkey --new"
}


def __getattr__(name):  # python 3.7+, otherwise define each script manually
    cmd = scripts.get(name, None)
    if not cmd:
        raise Exception("No script found")
    subprocess.run(cmd.split(" ") + sys.argv[1:])

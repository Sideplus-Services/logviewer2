import re
from logviewer2.constants import Constants


def GET_DCONFIG(cfg):
    obj = {}
    for (key, value) in cfg.items():
        match = re.match(Constants.RE_ENV_DISCORD, key)
        if match:
            obj[match.groups()[0]] = value
    return obj


def GET_MCONFIG(cfg):
    obj = {}
    for (key, value) in cfg.items():
        match = re.match(Constants.RE_ENV_MONGODB, key)
        if match:
            obj[int(match.groups()[0])] = value
    return obj
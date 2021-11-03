from logviewer2.constants import Constants


def GET_SECRET_KEY(config):
    key = config.get("FLASK_SECRET_KEY", None)
    if not key:
        from secrets import choice
        import string
        key = ''.join([choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50)])
        print("Cannot grab flask secret key from env, Generating a temp one")
        print("Use this key in Env if you want to presist sessions:\n" + key)
    return bytes(key, 'utf8')


def GET_REV():
    import subprocess
    REV = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    return str(REV, 'utf=8')[:7]


def GET_INSTANCE(qid):
    if not type(qid) is str:
        raise ValueError("incorrect itemtype")

    if qid.isdigit():
        return int(qid), 0
    elif qid:
        if "_" in qid:
            try:
                parts = list(map(int, qid.split('_')))
                return parts[0], parts[1]
            except ValueError:
                raise ValueError("one or both types are invalid (not ints)")
        else:
            raise ValueError("Incorrect string format")


def DOWNLOAD_FONTS():
    import tempfile
    import requests

    from pathlib import Path

    FDIR = tempfile.TemporaryDirectory()
    pFDIR = Path(FDIR.name)
    for name, file in Constants.FONTS.items():
        with requests.get(Constants.DISCORD_ASSISTS_URL + file, stream=True) as r:
            # noinspection PyBroadException
            try:
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                with open(Path.joinpath(pFDIR, name), 'wb') as f:
                    f.write(r.content)
            except:
                continue

    return FDIR


def GET_USERS_FROM_ROLES(role_cfg):
    users = []
    for role in role_cfg:
        users += role_cfg[role]
    return users

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


def DOWNLOAD_FONTS():
    import tempfile
    import requests

    from pathlib import Path
    from logviewer2.constants import Constants

    FDIR = tempfile.TemporaryDirectory()
    pFDIR = Path(FDIR.name)
    for name, file in Constants.FONTS.items():
        with requests.get(Constants.DISCORD_ASSISTS_URL + file, stream=True) as r:
            try:
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                with open(Path.joinpath(pFDIR, name), 'wb') as f:
                    f.write(r.content)
            except:
                continue

    return FDIR

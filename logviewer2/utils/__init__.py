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

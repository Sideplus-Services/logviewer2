import re


class Constants:
    RE_ENV_DISCORD = re.compile(r"DISCORD_(.*)")
    RE_ENV_MONGODB = re.compile(r"MONGO_URI_(.*)")
    RE_FPROXY_FACE = re.compile(r"/fproxy/(.*)")
    LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
    FONTS = {"gg_sans_normal400": "gg_sans_normal400.woff2",
             "gg_sans_italic400": "gg_sans_italic400.woff2",
             "gg_sans_normal500": "gg_sans_normal500.woff2",
             "gg_sans_italic500": "gg_sans_italic500.woff2",
             "gg_sans_normal600": "gg_sans_normal600.woff2",
             "gg_sans_italic600": "gg_sans_italic600.woff2",
             "gg_sans_normal700": "gg_sans_normal700.woff2",
             "gg_sans_italic700": "gg_sans_italic700.woff2",
             "gg_sans_normal800": "gg_sans_normal800.woff2",
             "gg_sans_italic800": "gg_sans_italic800.woff2"}

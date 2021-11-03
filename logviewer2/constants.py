import re


class Constants:
    RE_ENV_DISCORD = re.compile(r"DISCORD_(.*)")
    RE_ENV_MONGODB = re.compile(r"MONGO_URI_(.*)")
    RE_FPROXY_FACE = re.compile(r"/fproxy/(.*)")
    DISCORD_ASSISTS_URL = 'https://discordapp.com/assets/'
    LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
    FONTS = {"FONT_WHITNEY_LIGHT": "6c6374bad0b0b6d204d8d6dc4a18d820.woff",
             "FONT_WHITNEY_NORMAL": "e8acd7d9bf6207f99350ca9f9e23b168.woff",
             "FONT_WHITNEY_MEDIUM": "3bdef1251a424500c1b3a78dea9b7e57.woff",
             "FONT_WHITNEYMEDIUM_MEDIUM": "be0060dafb7a0e31d2a1ca17c0708636.woff",
             "FONT_WHITNEY_BOLD": "8e12fb4f14d9c4592eb8ec9f22337b04.woff"}

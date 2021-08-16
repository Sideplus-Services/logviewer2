import re


class Constants:
    RE_ENV_DISCORD = re.compile("DISCORD_(.*)")
    RE_ENV_MONGODB = re.compile("MONGO_URI_(.*)")
    LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'

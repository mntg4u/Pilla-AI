from os import environ
from dotenv import load_dotenv
import os
import time
import re

from os import environ
from dotenv import load_dotenv

import os, time, re
id_pattern = re.compile(r'^.\d+$')

load_dotenv()

API_ID = int(environ.get("API_ID", 0))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

ADMIN = [int(admin) for admin in environ.get('ADMIN', '1892771262').split()]
CHAT_GROUP = int(environ.get("CHAT_GROUP", 0))
LOG_CHANNEL = environ.get("LOG_CHANNEL", "-1002292607317")
MONGO_URL = environ.get("MONGO_URL", "")
AUTH_CHANNEL = environ.get("AUTH_CHANNEL", "-1002116310726")
FSUB = environ.get("FSUB", "True").lower() == "true"
STICKERS_IDS = ["CAACAgQAAxkBAAEK99dlfC7LDqnuwtGRkIoacot_dGC4zQACbg8AAuHqsVDaMQeY6CcRojME"]
COOL_TIMER = 20
ONLY_SCAN_IN_GRP = environ.get("ONLY_SCAN_IN_GRP", "True").lower() == "true"
REACTIONS = ["❤", "⚡",]

class Config(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_UPTIME = time.time()
    ADMIN = [int(admin) for admin in os.environ.get('ADMIN', '').split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
    WEBHOOK = os.environ.get("WEBHOOK", "True").lower() == "true"

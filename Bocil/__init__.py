# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import logging
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyromod import listen

from Bocil.config import API_HASH, API_ID, BOT_TOKEN, DB_URL, STRING_SESSION, SUDO_USERS

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

LOGS = logging.getLogger(__name__)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


if not STRING_SESSION:
    LOGGER(__name__).error("No String Session Found! Exiting!")
    sys.exit()

if not API_ID:
    LOGGER(__name__).error("No API_ID Found! Exiting!")
    sys.exit()

if not API_HASH:
    LOGGER(__name__).error("No API_HASH Found! Exiting!")
    sys.exit()

LOOP = asyncio.get_event_loop()

trl = Translator()

aiosession = ClientSession()

CMD_HELP = {}

scheduler = AsyncIOScheduler()

StartTime = time.time()

START_TIME = datetime.now()

TEMP_SETTINGS: Dict[Any, Any] = {}
TEMP_SETTINGS["PM_COUNT"] = {}
TEMP_SETTINGS["PM_LAST_MSG"] = {}

app = Client(
    name="BocilUserbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)
# useless
""" 
class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters=None, group=0):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        if self not in self._ubot:
            self._ubot.append(self)

"""
bot = Client(
    name="bot-bocil",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)
bots = [bot for bot in [bot] if bot]

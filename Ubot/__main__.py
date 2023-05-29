import importlib
import time
from datetime import datetime
import asyncio
from pyrogram import idle
from pyrogram.errors import RPCError
from uvloop import install
from Ubot import BOTLOG_CHATID, aiosession, bot1, bots, app, ids, LOOP, event_loop
from platform import python_version as py
from Ubot.logging import LOGGER
from pyrogram import __version__ as pyro

from Ubot.modules import ALL_MODULES
from Ubot.core.db import *
from config import SUPPORT, CHANNEL, CMD_HNDLR, ADMIN1_ID, ADMIN2_ID, ADMIN3_ID, ADMIN4_ID, ADMIN5_ID, ADMIN6_ID, ADMIN7_ID
import os
from dotenv import load_dotenv
from pyrogram.errors import RPCError
from Ubot.helper import join

MSG_BOT = """
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
**New Ubot Actived ✅**
**Phython**: `{}`
**Pyrogram**: `{}`
**User**: `{}`
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""

MSG_ON = """
**New Ubot Actived ✅**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
◉ **Versi** : `{}`
◉ **Phython** : `{}`
◉ **Pyrogram** : `{}`

**Ketik** `{}alive` **untuk Mengecheck Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""


async def main():
    await app.start()
    LOGGER("Ubot").info("Memulai Ubot Pyro..")
    for all_module in ALL_MODULES:
        importlib.import_module("Ubot.modules" + all_module)
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            LOGGER("Ubot").info("Startup Completed")
            LOGGER("√").info(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
            user = len(ids)
        except Exception as e:
            LOGGER("X").info(f"{e}")
            if "Telegram says:" in str(e):
                load_dotenv()
                session_name = None
                for i in range(1, 201):
                    if os.getenv(f"SESSION{i}") == str(e):
                        session_name = f"SESSION{i}"
                        os.environ.pop(session_name)
                        LOGGER("Ubot").info(f"Removed {session_name} from .env file due to error.")
                        await bot.send_message("me", f"Removed {session_name} from .env file due to error.")
                        break
                if session_name is None:
                   LOGGER("Ubot").info(f"Could not find session name in .env file for error: {str(e)}")
    #await bot.send_message("me", MSG_BOT.format(py(), pyro, user))
    await idle()
    await aiosession.close()
    


              

if __name__ == "__main__":
    LOGGER("Ubot").info("Starting  Ubot")
    install()
#    LOOP.run_until_complete(main())
    event_loop.run_until_complete(main())

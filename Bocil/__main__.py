# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import importlib

from pyrogram import idle
from uvloop import install

from Bocil import LOGGER, LOOP, aiosession, app, bots
from Bocil.config import BOT_VER, BOTLOG_CHATID, HANDLER
from Bocil.helpers.misc import heroku
from Bocil.modules import ALL_MODULES

MSG_ON = """
🔥 **Bocil-Userbot Berhasil Di Aktifkan**
━━
➠ **Userbot Version -** `{}`
➠ **Ketik** `{}alive` **untuk Mengecheck Bot**
━━
"""


async def main():
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module(f"Bocil.modules.{all_module}")
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            try:
                await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, HANDLER))
            except BaseException:
                pass
            LOGGER("Bocil").info(f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]")
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("Bocil").info(f"Bocil-UserBot v{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    """
    await app.start()
    print(f"Bot Started @{app.me.username}")
    await bot.start()
    print(f"Ubot Started @{bot.me.username}")
    await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, HANDLER))
    if bot and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot)
    for all_module in ALL_MODULES:
        importlib.import_module(f"Bocil.modules.{all_module}")    
    for _bot in get_userbots():
        bots = Ubot(**_bot)
        try:
            await bots.start()
            LOGGER("Bocil").info(
                f"Logged in as {bots.me.first_name} | [ {bots.me.id} ]"
            )
    
        except RPCError as a:
            LOGGER("main").warning(a)
    LOGGER("Bocil").info(f"Bocil-UserBot v{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    
    await idle()
    """
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Bocil").info("Starting Bocil-UserBot")
    install()
    heroku()
    LOOP.run_until_complete(main())

# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from gpytranslate import Translator
from pyrogram import filters

from Bocil import bot
from Bocil.config import HANDLER as cmd

from .help import add_command_help


@bot.on_message(filters.me & filters.command(["tr", "trt", "translate"], cmd))
async def translates(client, message):
    trans = Translator()
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Balas pesan untuk menerjemahkannya!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"**Diterjemahkan dari {source} ke {dest}**:\n" f"`{translation.text}`"
    await message.reply_text(reply)


add_command_help(
    "translate",
    [
        [
            "tr <kode bahasa> <text/reply>",
            "Menerjemahkan teks ke bahasa yang disetel. (Default kode bahasa indonesia)",
        ],
    ],
)

# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from datetime import datetime

from pyrogram import filters
from pyrogram.types import *

from Bocil import CMD_HELP, app, bot
from Bocil.config import ADMIN, HANDLER, OWNER_ID
from Bocil.helpers.SQL.ubot_sql import get_habis

from .help import add_command_help


@bot.on_message(filters.command("alive", HANDLER) & filters.me)
async def alive_cmd(client, message):
    nice = await client.get_inline_bot_results(app.me.username, message.command[0])
    await message.reply_inline_bot_result(nice.query_id, nice.results[0].id)


@app.on_inline_query(filters.regex("alive"))
async def alive_bot(client, inline_query):
    start = datetime.now()
    ea = await app.get_users(inline_query.from_user.id)
    dc_id = f"{ea.dc_id}" if ea.dc_id else "-"
    habis = get_habis(ea.id)
    kd = "-"
    if habis is not None:
        for i in habis:
            kd = i.habis
    if ea.id in OWNER_ID:
        status = "Owner"
    elif ea.id in ADMIN:
        status = "Admin"
    else:
        status = "Member"
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    msg = f"""
**Bocil Userbot**
    **status:** **__Premium [{status}]__**
        **dc:** `{dc_id}`
        **experied:** `{kd}`
        **Total Modules:** `{len(CMD_HELP)}` Modules 
        **ping_dc:** `{duration} ms`
"""
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    thumb_url="https://telegra.ph//file/deaf5d4f775190f8ce461.jpg",
                    title="Alive",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "⟨ Support ⟩", url="t.me/Pantekyks"
                                ),
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


add_command_help(
    "alive",
    [
        [
            f"alive",
            "Untuk Menampilkan batas waktu bot.",
        ]
    ],
)

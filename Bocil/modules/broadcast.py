# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get

from Bocil import bot
from Bocil.config import HANDLER as cmd
from Bocil.helpers.adminHelpers import DEVS
from Bocil.helpers.basic import edit_or_reply
from Bocil.helpers.SQL.broad_sql import add_chat, del_chat, get_chat
from Bocil.helpers.tools import get_arg

from .help import add_command_help

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/Hamam22/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001473548283, -1001390552926, -1001704645461]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST


@bot.on_message(filters.command("gcast", cmd) & filters.me)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "`Started global broadcast...`")
    else:
        return await message.edit_text("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    bl = get_chat(str(client.me.id))
    if not bl:
        add_chat(client.me.id, message.chat.id)
    black = []
    for i in bl:
        bk = i.chat_id
        black.append(bk)
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await message.reply("mohon balas sesuatu atau ketik sesuatu")
                else:
                    msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST and chat not in black:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    else:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Man.edit_text(
        f"💬 Mengirim Pesan Global\n\n✅ Berhasil Terkirim: {done} \n❌ Gagal Terkirim: {error}"
    )


@bot.on_message(filters.command("gucast", cmd) & filters.me)
async def gucast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "`Started global broadcast...`")
    else:
        return await message.edit_text("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Man.edit_text(
        f"💬 Mengirim Pesan Global\n\n✅ Berhasil Terkirim: {done} \n❌ Gagal Terkirim: {error}"
    )


@bot.on_message(filters.command("blchat", cmd) & filters.me)
async def blchatgcast(client: Client, message: Message):
    chat = get_chat(str(client.me.id))
    if not chat:
        return await message.reply("**Tidak ada daftar blacklist chat.**")
    msg = f"**Daftar blacklist gcast**\n"
    for i in chat:
        msg += f"* `{i.chat_id}`\n"
    await message.reply(msg)


@bot.on_message(filters.command("addblacklist", cmd) & filters.me)
async def addblacklist(client: Client, message: Message):
    iya = await message.reply("Processing")
    add_chat(client.me.id, message.chat.id)
    await iya.edit(f"Berhasil menambahkan {message.chat.id} ke Blacklist gcast")


@bot.on_message(filters.command("delblacklist", cmd) & filters.me)
async def delblacklist(client: Client, message: Message):
    iya = await message.reply("Processing")
    del_chat(client.me.id, message.chat.id)
    await iya.edit(f"Berhasil menghapus {message.chat.id} dari Blacklist gcast")


add_command_help(
    "broadcast",
    [
        [
            "gcast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "gucast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "blchat",
            "Untuk Mengecek informasi daftar blacklist gcast.",
        ],
        [
            "addblacklist",
            "Untuk Menambahkan grup tersebut ke blacklist gcast.",
        ],
        [
            "delblacklist",
            f"Untuk Menghapus grup tersebut dari blacklist gcast.\n\n  •  **Note :** Ketik perintah `.addblacklist` dan `.delblacklist` di grup yang kamu Blacklist.",
        ],
    ],
)

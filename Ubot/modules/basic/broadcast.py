#izzy
import asyncio
import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from Ubot.helper import edit_or_reply
from . import *
from Ubot.helper import *
from Ubot.database.accesdb import *
from config import *
from geezlibs import BL_GCAST


HAPP = None

@Ubot("gcast", cmds)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        await message.edit_text("`Memulai Gcast...`")
    else:
        return await message.edit_text("**Balas ke pesan/berikan sebuah pesan**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in BL_GCAST and chat not in BLACKLIST_GCAST:
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
    await message.edit_text(
        f"**Berhasil mengirim ke** `{done}` **Groups chat, Gagal mengirim ke** `{error}` **Groups**"
    )

@Ubot("gucast", cmds)
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        await message.edit_text("`Started global broadcast...`")
    else:
        return await message.edit_text("**Berikan sebuah pesan atau balas ke pesan**")
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
    await message.edit_text(
        f"**Successfully Sent Message To** `{done}` **chat, Failed to Send Message To** `{error}` **chat**"
    )


@Ubot("addbl", cmds)
async def addblacklist(client: Client, message: Message):
    await message.edit_text("`Processing...`")
    if HAPP is None:
        return await message.edit_text(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
    blgc = f"{BLACKLIST_GCAST} {message.chat.id}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await message.edit_text(
        f"**Berhasil Menambahkan** `{message.chat.id}` **ke daftar blacklist gcast.**\n\nSedang MeRestart ntuk Menerapkan Perubahan."
    )
    if await in_heroku():
        heroku_var = HAPP.config()
        heroku_var["BLACKLIST_GCAST"] = blacklistgrup
    else:
        path = dotenv.find_dotenv()
        dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
    restart()

@Ubot("delbl", cmds)
async def delblacklist(client: Client, message: Message):
    await message.edit_text("`Processing...`")
    if HAPP is None:
        return await message.edit_text(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
    blchat = f"{BLACKLIST_GCAST} {message.chat.id}"
    gett = str(message.chat.id)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await message.edit_text(
            f"**Berhasil Menghapus** `{message.chat.id}` **dari daftar blacklist gcast.**\n\nSedang MeRestart untuk Menerapkan Perubahan."
        )
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BLACKLIST_GCAST"] = blacklistgrup
        else:
            path = dotenv.find_dotenv()
            dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
        restart()
    else:
        await message.edit_text("**Grup ini tidak ada dalam daftar blacklist gcast.**")


add_command_help(
    "broadcast",
    [
        [f"gcast [text/reply]",
            "Broadcast pesan ke Group. (bisa menggunakan Media/Sticker)"],
        [f"gucast [text/reply]",
            "Broadcast pesan ke semua chat. (bisa menggunakan Media/Sticker)"],
        [f"addbl [id group]",
            "menambahkan group ke dalam blacklilst gcast"],
        [f"delbl [id group]",
            "menghapus group dari blacklist gcast"],
    ],
)

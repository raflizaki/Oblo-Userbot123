#izzy
import asyncio
import random
from datetime import datetime
from platform import python_version
from . import *
from Ubot.helper.PyroHelpers import ReplyCheck
from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from config import ALIVE_PIC, ALIVE_TEXT
from Ubot import START_TIME, SUDO_USER, app
from Ubot.database.accesdb import *
from Ubot.modules.bot.inline import get_readable_time

BOT_VER = "0.01"
alive_logo = ALIVE_PIC or ""

if ALIVE_TEXT:
   txt = ALIVE_TEXT
else:
    txt = (
         f"▰▱▰▱°▱▱°▱▰▱▰\n"
        f" ◉ **Bocil-Userbot**\n\n"
        f" ◉ **Versi**: `{BOT_VER}`\n"
        f" ◉ **Uptime**: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f" ◉ **Phython**: `{python_version()}`\n"
        f" ◉ **Pyrogram**: `{__version__}`\n"
        f" ▰▱▰▱°▱▱°▱▰▱▰\n"
    )

@Client.on_message(filters.command("alive", ["?", "!", ".", "-", "*", "^"]) & filters.me)
async def alive(client: Client, message: Message):
    bot_username = (await app.get_me()).username
    try:
        shin = await client.get_inline_bot_results(bot=bot_username, query=f"alive {id(message)}")
        await asyncio.gather(
            client.send_inline_bot_result(
                message.chat.id, shin.query_id, shin.results[0].id, reply_to_message_id=message.id
            )
        )
    except Exception as e:
        print(f"{e}")


@Ubot("id", cmds)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`"
            file_id += "**File Type**: `audio`"

        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`"
            file_id += f"**File Type**: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`"
            file_id += "**File Type**: `photo`"

        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker**: `False`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"

        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += "**File Type**: `video`"

        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `GIF`"

        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += "**File Type**: `Voice Note`"

        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `Video Note`"

        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**Message ID**: `{message.reply_to_message.id}`\n"
            user_detail += f"**Your ID**: `{message.from_user.id}`\n"
            user_detail += f"**Chat ID**: `{message.chat.id}`\n\n"
            user_detail += f"**Your ID**: `{message.from_user.id}`\n"
            user_detail += f"**Replied Message ID**: `{message.reply_to_message.id}`\n"
            user_detail += f"**Replied User ID**: `{message.reply_to_message.from_user.id}`\n"
        await message.edit(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await message.edit(user_detail)

    else:
        await message.edit(f"**Chat ID**: `{message.chat.id}`")

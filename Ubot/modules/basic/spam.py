import asyncio
from threading import Event
from pyrogram import Client, enums
from pyrogram.types import Message
from Ubot.helper import extract_args, edit_or_reply
from . import *

SPAM_COUNT = [0]
def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50


@Ubot("dspam", cmds)
async def delayspam(client: Client, message: Message):
    #if message.chat.id in BL_GCAST:
    #    return await edit_or_reply(
    #        message, "**Gabisa Digunain Disini Tod!!**"
    #    )
    delayspam = await extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await message.edit(f"`Format salah,\ngunakan {cmds}dspam [waktu] [jumlahspam] [kata-kata]`")
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message(
        "me", "**#DELAYSPAM**\nDelaySpam was executed successfully"
    )

async def spam_stick(client: Client, message: Message):
    if not message.reply_to_message:
        await edit_or_reply(
            message, "**reply to a sticker with amount you want to spam**"
        )
        return
    if not message.reply_to_message.sticker:
        await edit_or_reply(
            message, "**reply to a sticker with amount you want to spam**"
        )
        return
    else:
        i = 0
        times = message.command[1]
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)

add_command_help(
    "spam",
    [
        [f"{cmds}dspam [waktu delay] [jumlah] [kata-kata]","delay spam"],
        [f"{cmds}sspam [balas ke stiker] [jumlah spam]", "spam stiker"],
    ],
)
#izzy

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
from Ubot.database.accesdb import *


@Ubot("dm", cmds)
@check_access
async def dm(coli: Client, memek: Message):
    Ubot = await memek.reply_text("` Proccessing.....`")
    quantity = 1
    inp = memek.text.split(None, 2)[1]
    user = await coli.get_chat(inp)
    spam_text = ' '.join(memek.command[2:])
    quantity = int(quantity)

    if memek.reply_to_message:
        reply_to_id = memek.reply_to_message.message_id
        for _ in range(quantity):
            await Ubot.edit("Message Sended Successfully !")
            await coli.send_message(user.id, spam_text,
                                      reply_to_messsge_id=reply_to_id)
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await coli.send_message(user.id, spam_text)
        await Ubot.edit("Message Sended Successfully !")
        await asyncio.sleep(0.15)


add_command_help(
    "dm",
    [
        [f"dm @username kata", "Untuk Mengirim Pesan Tanpa Harus Kedalam Roomchat.",],
    ],
)

from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Bocil import bot
from Bocil.config import HANDLER as cmd
from Bocil.helpers.basic import edit_or_reply
from Bocil.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


@bot.on_message(filters.command(["asupan", "ptl"], cmd) & filters.me)
async def asupan_cmd(client: Client, message: Message):
    Man = await edit_or_reply(message, "`Tunggu Sebentar...`")
    await gather(
        Man.delete(),
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        "tedeasupancache", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )


add_command_help(
    "asupan",
    [
        [
            f"asupan atau .ptl",
            "Untuk Mengirim video asupan secara random.",
        ]
    ],
)

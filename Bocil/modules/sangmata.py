# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de


from asyncio import sleep

from pyrogram import filters

from Bocil import bot
from Bocil.config import HANDLER as cmd
from Bocil.utils import extract_user

from .help import add_command_help


@bot.on_message(filters.command(["sg", "sa", "sangmata"], cmd) & filters.me)
async def sangmata(c, m):
    user_id = await extract_user(m)
    if not user_id:
        return await m.reply("Silahkan balas atau kombinasikan dengan id atau username")
    sg_i = await m.reply("**🔍 Sedang Memeriksa**")
    await c.unblock_user("@SangMata_beta_bot")
    sg_m = await c.send_message("@SangMata_beta_bot", f"{user_id}")
    await sg_m.delete()
    await sleep(3)
    async for msg in c.search_messages("@SangMata_beta_bot", query="Names"):
        if not msg:
            await sg_i.edit("**Orang Ini Belum Pernah Mengganti Namanya**")
            return
        elif msg:
            await msg.copy(m.chat.id, reply_to_message_id=m.id)
            await msg.delete()
            await sg_i.delete()


add_command_help(
    "sangmata",
    [
        [
            f"sg <reply/userid/username>",
            "Untuk Mendapatkan Riwayat Nama Pengguna selama di telegram.",
        ],
    ],
)

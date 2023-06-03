# Credits Thx Tomi Setiawan


from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import RPCError
from pyrogram.enums import ChatType
from . import *
from Ubot import cmds, app
from Ubot.helper import get_arg



@Client.on_message(filters.me & filters.command("nyolong", cmds))
async def nyolongnih(client, message):
    link = get_arg(message)
    if not link:
        return await message.reply("Silahkan kombinasikan command dan link")
    au = await message.reply("Nyolong konten dulu cuy")
    if link.startswith("https"):
        if "?single" in link:
            link_ = link.split("?single")[0]
            msg_id = int(link_.split("/")[-1])
        else:
            msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                await au.edit("Sepertinya ada yang salah")
            try:
                await client.copy_message(
                    message.chat.id, chat, msg_id, reply_to_message_id=message.id
                )
                await au.delete()
            except:
                await colong(client, message, dia)
            await au.delete()
        else:
            try:
                chat = str(link.split("/")[-2])
                hah = await client.get_chat(chat)
            except RPCError:
                await au.edit("Sepertinya ada yang salah")
            if hah.type == ChatType.CHANNEL:
                dia = await app.get_messages(chat, msg_id)
                await client.unblock_user(app.me.username)
                await dia.copy(message.from_user.id)
                await sleep(2)
                async for enak in client.get_chat_history(app.me.username, 1):
                    await enak.copy(message.chat.id, reply_to_message_id=message.id)
                    await au.delete()
                    await enak.delete()
            else:
                try:
                    await client.copy_message(
                        message.chat.id, chat, msg_id, reply_to_message_id=message.id
                    )
                    await au.delete()
                except:
                    dia = await client.get_messages(chat, msg_id)
                    await colong(client, message, dia)
                    await au.delete()

    else:
        await au.edit("Sepertinya ada yang salah")


@Client.on_message(filters.me & filters.command("curi", cmds))
async def curinih(client, message):
    if not message.reply_to_message:
        return await message.reply("Silahkan balas ke pesan")
    anu = await client.download_media(message.reply_to_message)
    await message.delete()
    if message.reply_to_message.photo:
        await client.send_photo("me", anu)
        os.remove(anu)
    elif message.reply_to_message.video.file_size > 10000000:
        return await message.reply("File terlalu besar lebih dari 10 mb")
    await client.send_video("me", anu)
    os.remove(anu)


async def colong(client, message, dia):
    anjing = dia.caption or None
    if dia.text:
        await dia.copy(message.chat.id, reply_to_message_id=message.id)
    if dia.sticker:
        await dia.copy(message.chat.id, reply_to_message_id=message.id)
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)
    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)
    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)
    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)
    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)
    if dia.animation:
        anu = await client.download_media(dia)
        await client.send_animation(
            message.chat.id, anu, anjing, reply_to_message_id=message.id
        )
        os.remove(anu)



add_command_help(
    "nyolong",
    [
        [f"nyolong", "nyolong konten orang"],
    ],
)

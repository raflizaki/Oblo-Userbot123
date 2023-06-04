import io
from io import *
import os
import requests
import openai
import shutil
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified
from . import *
from Ubot.core.func import *
from Ubot.database.accesdb import *
from asyncio import gather
from Ubot.core.what import *
from Ubot.core.ai import OpenAi
from config import OPENAI_API_KEY


RMBG_API_KEY = "3RCCWg8tMBfDWdAs44YMfJmC"

API = "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".split()
        

@Ubot(["ai", "ask"], cmds)
async def openai(c, m):
    openai.api_key = random.choice(API)
    if len(m.command) == 1:
        return await m.reply(f"Ketik <code>{prefix}{m.command[0]} [question]</code> Pertanyaan untuk menggunakan OpenAI")
    question = m.text.split(" ", maxsplit=1)[1]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    json_data = {
        "model": "text-davinci-003",
        "prompt": question,
        "max_tokens": 500,
        "temperature": 0,
    }
    msg = await m.reply("`Processing..")
    try:
        response = (await http.post("https://api.openai.com/v1/completions", headers=headers, json=json_data)).json()
        await msg.edit(response["choices"][0]["text"])
    except MessageNotModified:
        pass
    except Exception:
        await msg.edit("`Data tidak ditemukan, pastikan OPENAI_API valid...`")

@Ubot(["img", "photo"], cmds)
async def _(client, message):
    Tm = await message.reply("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b><code>{message.text}</code> [query]</b>")
    try:
        response = OpenAi.Photo(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()
        
@Ubot("rmbg", cmds)
async def rmbg_background(c: Client, m: Message):
    api_key = RMBG_API_KEY
    reply = m.reply_to_message
    ky = await m.reply("`Processing..")
    photo_id = m.reply_to_message.photo.file_id
    if not (reply and (reply.media)):
      return await m.edit("`Mohon balas ke foto...`")
    temp_file = await c.download_media(photo_id)
    if not api_key:
       return await m.edit("**RMBG_API_KEY: missing**")
    endpoint = "https://api.remove.bg/v1.0/removebg"
    payload = {"size": "auto"}

    if api_key:
       with open(temp_file, "rb") as image_file:
          response = requests.post(endpoint, data=payload, headers={"X-Api-Key": api_key}, files={"image_file": image_file}, stream=True)

    with open("output.png", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    await m.reply_document("output.png")
    try:
       clear_file = "ky.webp"
       clear_file2 = "output.png"
       (await shell_exec("cp *.png ky.webp"))[0]
       await c.send_sticker(m.chat.id, "ky.webp")
       os.remove(clear_file)
       os.remove(clear_file2)
    except BaseException:
        pass


add_command_help(
    "openai",
    [
        [f"ask or ai [pertanyaan]", "Chat Open AI."],
    ],
)


add_command_help(
    "image",
    [
        [f"img or photo [query]", "Untuk mengunduh gambar yang dicari."],
        [f"rmbg [reply photo]", "Untuk menghapus background pada gambar."],
        [f"toanime <reply to foto>", "Convert foto ke anime menggunakan ai bot"],
        [f"toimg <reply stiker>", "Convert stiker ke foto."],
        [f"cartoon [reply to image]", "Ubah gambar menggunakan deepai api."],
        [f"toonify [reply to image]", "Untuk mempercantik gambar menggunakan deepai api."],
        [f"face [reply to image]", "Untuk memeriksa deteksi wajah."],
    ],
)



import asyncio
import random

import Ubot.modules.basic.truth_and_dare_string as tod

from . import *


# LU GABISA CODING LU KONTOL
# BELAJAR CODING DARI NOL
@Ubot("apakah", cmds)
async def apakah(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.AP)}")



@Ubot("kenapa", cmds)
async def kenapa(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.KN)}")


@Ubot("bagaimana", cmds)
async def bagaimana(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.BG)}")


@Ubot("dare", cmds)
async def dare(client, message):
    try:        
        await message.edit(f"{random.choice(tod.DARE)}")
    except BaseException:
        pass


@Ubot("truth", cmds)
async def truth(client, message):
    try:
        await message.edit(f"{random.choice(tod.TRUTH)}")
    except Exception:
        pass


add_command_help(
    "dare",
    [
        [f"dare", "Coba sendiri"],
        [f"truth", "Coba sendiri"],
        [f"apakah [pertanyaan]", "Coba sendiri"],
        [f"kenapa [pertanyaan]", "Coba sendiri"],
        [f"bagaimana [pertanyaan]", "Coba sendiri"],
    ],
)
        

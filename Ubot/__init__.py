import asyncio
import logging
import sys
import time
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Ubot.get_config import get_config
from config import *
cmds = ["!", "?", "*", "-", "^", "."]
CMD_HELP = {}
clients = []
ids = []

SUDOERS = filters.user()
SUDO_USER = SUDOERS


if BOTLOG_CHATID:
   BOTLOG_CHATID = BOTLOG_CHATID
else:
   BOTLOG_CHATID = "me"


SUDO_USER = SUDOERS
trl = Translator()
aiosession = ClientSession()
CMD_HELP = {}
scheduler = AsyncIOScheduler()
StartTime = time.time()
START_TIME = datetime.now()
TEMP_SETTINGS: Dict[Any, Any] = {}
TEMP_SETTINGS["PM_COUNT"] = {}
TEMP_SETTINGS["PM_LAST_MSG"] = {}

LOOP = asyncio.get_event_loop_policy()
event_loop = LOOP.get_event_loop()
asyncio.set_event_loop(event_loop)


# event_policy = asyncio.get_event_loop_policy()
# event_loop = event_policy.get_event_loop()
# asyncio.set_event_loop(event_loop)


BOT_WORKERS = int(get_config("BOT_WORKERS", "4"))
COMMM_AND_PRE_FIX = get_config("COMMM_AND_PRE_FIX", "/")
START_COMMAND = get_config("START_COMMAND", "deploy")
SESI_COMMAND = get_config("SESI_COMMAND", "tampil")
SESIID_COMMAND = get_config("SESI_COMMAND", "cari")
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "Ubot.log")

AKTIFSESI = {}
# /start message when other users start your bot
SESI_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        TAMPIL SESI : 
        """
    )
)
AKTIFSESIID = {}
# /start message when other users start your bot
SESIID_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        Fitur ini untuk cari sesi string yang sudah menggunakan bot ini
        """
    )
)
AKTIFPERINTAH = {}
START_OTHER_USERS_TEXT = get_config(
    "START_OTHER_USERS_TEXT",
    (
        f"""
        👋 **Halo Saya Adalah New-Ubot Pyro**
        """
    )
)
INPUT_PHONE_NUMBER = get_config("INPUT_PHONE_NUMBER", (
    "Masukan nomor akun telegram anda dengan diawali +, Contoh +62xxxx"
))
RECVD_PHONE_NUMBER_DBP = get_config("RECVD_PHONE_NUMBER_DBP", (
    "Mohon periksa pesan masuk anda, dan masukkan kode yang ada dengan menggunakan spasi setiap kode\n Contoh : 1 2 3 4 5"
))
ALREADY_REGISTERED_PHONE = get_config("ALREADY_REGISTERED_PHONE", (
    "Mencoba mengirikan kode OTP"
))
CONFIRM_SENT_VIA = get_config("CONFIRM_SENT_VIA", (
    "Mohon periksa pesan masuk anda, dan masukkan kode yang ada dengan menggunakan spasi setiap kode\n Contoh : 1 2 3 4 5 {}"
))
RECVD_PHONE_CODE = get_config("RECVD_PHONE_CODE", (
    "Mencoba mengirikan kode OTP"
))
NOT_REGISTERED_PHONE = get_config("NOT_REGISTERED_PHONE", (
    "Maaf Nomor Yang Anda Masukkan Belum Terdaftar"
))
PHONE_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
TFA_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
ACC_PROK_WITH_TFA = get_config("ACC_PROK_WITH_TFA", (
    "Verifikasi 2 Langkah Diaktifkan, Mohon Masukkan Verifikasi 2 Langkah Anda."
))
SESSION_GENERATED_USING = get_config("SESSION_GENERATED_USING", (
    "Ubot sudah aktif, Hubungi Admins Untuk MeRestart Bot ..."
))

if not BOT_TOKEN:
   LOGGER(__name__).error("WARNING: BOT TOKEN TIDAK DITEMUKAN, SHUTDOWN BOT")
   sys.exit()


app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=5,
    plugins=dict(root="Ubot/modules/bot"),
    in_memory=True,
)


bot1 = (
    Client(
        name="bot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION1,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION1
    else None
)

bot2 = (
    Client(
        name="bot2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION2,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION2
    else None
)

bot3 = (
    Client(
        name="bot3",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION3,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION3
    else None
)

bot4 = (
    Client(
        name="bot4",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION4,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION4
    else None
)

bot5 = (
    Client(
        name="bot5",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION5,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION5
    else None
)
bot6 = (
    Client(
        name="bot6",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION6,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION6
    else None
)

bot7 = (
    Client(
        name="bot7",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION7,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION7
    else None
)

bot8 = (
    Client(
        name="bot8",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION8,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION8
    else None
)

bot9 = (
    Client(
        name="bot9",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION9,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION9
    else None
)

bot10 = (
    Client(
        name="bot10",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION10,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION10
    else None
)

bot11 = (
    Client(
        name="bot11",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION11,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION11
    else None
)

bot12 = (
    Client(
        name="bot12",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION12,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION12
    else None
)

bot13 = (
    Client(
        name="bot13",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION13,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION13
    else None
)

bot14 = (
    Client(
        name="bot14",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION14,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION4
    else None
)

bot15 = (
    Client(
        name="bot15",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION15,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION15
    else None
)

bot16 = (
    Client(
        name="bot16",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION16,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION16
    else None
)

bot17 = (
    Client(
        name="bot17",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION17,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION17
    else None
)

bot18 = (
    Client(
        name="bot18",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION18,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION18
    else None
)

bot19 = (
    Client(
        name="bot19",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION19,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION19
    else None
)

bot20 = (
    Client(
        name="bot20",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION20,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION20
    else None
)
bot21 = (
    Client(
        name="bot21",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION21,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION21
    else None
)

bot22 = (
    Client(
        name="bot22",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION22,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION22
    else None
)

bot23 = (
    Client(
        name="bot23",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION23,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION23
    else None
)

bot24 = (
    Client(
        name="bot24",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION24,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION24
    else None
)

bot25 = (
    Client(
        name="bot25",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION25,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION25
    else None
)

bot26 = (
    Client(
        name="bot26",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION26,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION26
    else None
)

bot27 = (
    Client(
        name="bot27",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION27,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION27
    else None
)

bot28 = (
    Client(
        name="bot28",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION28,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION28
    else None
)

bot29 = (
    Client(
        name="bot29",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION29,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION29
    else None
)

bot30 = (
    Client(
        name="bot30",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION30,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION30
    else None
)

bot31 = (
    Client(
        name="bot31",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION31,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION31
    else None
)

bot32 = (
    Client(
        name="bot32",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION32,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION32
    else None
)

bot33 = (
    Client(
        name="bot33",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION33,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION33
    else None
)

bot34 = (
    Client(
        name="bot34",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION34,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION34
    else None
)

bot35 = (
    Client(
        name="bot35",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION35,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION35
    else None
)

bot36 = (
    Client(
        name="bot36",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION36,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION36
    else None
)

bot37 = (
    Client(
        name="bot37",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION37,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION37
    else None
)

bot38 = (
    Client(
        name="bot38",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION38,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION38
    else None
)

bot39 = (
    Client(
        name="bot39",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION39,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION39
    else None
)

bot40 = (
    Client(
        name="bot40",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION40,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION40
    else None
)

bot41 = (
    Client(
        name="bot41",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION41,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION41
    else None
)

bot42 = (
    Client(
        name="bot42",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION42,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION42
    else None
)

bot43 = (
    Client(
        name="bot43",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION43,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION43
    else None
)

bot44 = (
    Client(
        name="bot44",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION44,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION44
    else None
)

bot45 = (
    Client(
        name="bot45",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION45,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION45
    else None
)
bot46 = (
    Client(
        name="bot46",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION46,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION46
    else None
)

bot47 = (
    Client(
        name="bot47",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION47,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION47
    else None
)

bot48 = (
    Client(
        name="bot48",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION48,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION48
    else None
)

bot49 = (
    Client(
        name="bot49",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION49,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION49
    else None
)





bots = [bot for bot in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10, bot11, bot12, bot13, bot14, bot15, bot16, bot17, bot18, bot19, bot20, bot21, bot22, bot23, bot24, bot25, bot26, bot27, bot28, bot29, bot30, bot31, bot32, bot33, bot34, bot35, bot36, bot37, bot38, bot39, bot40, bot41, bot42, bot43, bot44, bot45, bot46, bot47, bot48, bot49, bot50] if bot]

for bot in bots:
    if not hasattr(bot, "group_call"):
        setattr(bot, "group_call", GroupCallFactory(bot).get_group_call())

# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from os import getenv

from dotenv import load_dotenv

load_dotenv("config.env")


API_HASH = getenv("API_HASH")
API_ID = int(getenv("API_ID", ""))
PM_LIMIT = int(getenv("PM_LIMIT", "5"))
BLACKLIST_CHAT = getenv("BLACKLIST_CHAT", None)
if not BLACKLIST_CHAT:
    BLACKLIST_CHAT = [-1001473548283]
BLACKLIST_GCAST = {int(x) for x in getenv("BLACKLIST_GCAST", "").split()}
BOTLOG_CHATID = int(getenv("BOTLOG_CHATID") or 0)
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))

BOT_VER = "0.2.0@main"
BRANCH = getenv("BRANCH", "main")
CHANNEL = getenv("CHANNEL", "gcaika")
HANDLER = getenv("HANDLER", ". ^ + - , ; ! ?").split()
DB_URL = getenv("DATABASE_URL", "")
GIT_TOKEN = getenv("GIT_TOKEN", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
GROUP = getenv("GROUP", "pantekyks")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
PMPERMIT_PIC = getenv("PMPERMIT_PIC", None)
REPO_URL = getenv("REPO_URL", "https://github.com/Hamam22/Bocil-Userbot")
STRING_SESSION = getenv("STRING_SESSION", "")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
MEMBERS = list(map(int, getenv("MEMBERS", "").split()))
ADMIN = list(map(int, getenv("ADMIN", "").split()))

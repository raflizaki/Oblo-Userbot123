from pyrogram.types import InlineKeyboardButton, WebAppInfo

class Data:

    text_help_menu = (
        f"**Help Menu**\n** • Prefixes** : `!`, `?`, `-`, `^`, `.`"
    )
    reopen = [[InlineKeyboardButton("Open", callback_data="reopen")]]

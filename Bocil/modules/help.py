# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from pyrogram import enums, filters

from Bocil import CMD_HELP, app, bot
from Bocil.config import HANDLER
from Bocil.helpers.basic import edit_or_reply
from Bocil.helpers.tools import get_arg


@bot.on_message(filters.command("help", HANDLER) & filters.me)
async def help(client, message):
    help_arg = get_arg(message)
    if not help_arg:
        nice = await client.get_inline_bot_results(app.me.username, message.command[0])
        await message.reply_inline_bot_result(nice.query_id, nice.results[0].id)

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"──「 **Help For {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `.{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "© @pantekyks"
            await edit_or_reply(
                message, this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **Bukan Nama Modul yang Valid.**",
            )


def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict

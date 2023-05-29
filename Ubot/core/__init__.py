from pyrogram import Client, filters
from Ubot import cmds
from pyrogram.types import Message

def Ubot(command: str, prefixes: cmds):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper

def Devs(command: str):
    def wrapper(func):
        @Client.on_message(filters.command(command, ".") & filters.user(DEVS))
        def wrapped_func(client, message):
            return func(client, message)

        return wrapped_func

    return wrapper


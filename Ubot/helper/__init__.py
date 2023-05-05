import os
import sys
from Ubot.helper.adminHelpers import *
from Ubot.helper.aiohttp_helper import *
from Ubot.helper.basic import *
from Ubot.helper.constants import *
from Ubot.helper.data import *
from Ubot.helper.inline import *
from Ubot.helper.parser import *
from Ubot.helper.PyroHelpers import *
from Ubot.helper.utility import *
from Ubot.helper.what import *
from Ubot.helper.misc import *
from Ubot.helper.tools import *


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])

async def join(client):
    try:
        await client.join_chat("GeezRam")
    except BaseException:
        pass

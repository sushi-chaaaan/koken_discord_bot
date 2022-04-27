import os
import sys
import traceback
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands
from dotenv import load_dotenv

from logger import getMyLogger

load_dotenv()

logger = getMyLogger(__name__)

utc = timezone.utc
jst = timezone(timedelta(hours=9), "Asia/Tokyo")

token = os.environ["DISCORD_TOKEN"]

EXT_LIST = [
    "cogs.error",
    "cogs.markdown_pdf",
]

intents = discord.Intents.all()
intents.typing = False

discord.http.API_VERSION = 9


class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="!h", description="HappiBot", intents=intents, **kwargs
        )
        self.persistent_views_added = False
        for cog in EXT_LIST:
            try:
                self.load_extension(cog)
                print(f"Extension [{cog}.py] is loaded!")
            except Exception:
                traceback.print_exc()
                logger.exception(f"Failed to load extension [{cog}.py]")

    async def on_connect(self):
        await self.sync_commands()

    async def on_ready(self):

        # add persistent views
        if not self.persistent_views_added:
            VIEWS = []
            for view in VIEWS:
                try:
                    self.add_view(view)
                    print(f"Added View [{view}] !")
                except Exception:
                    traceback.print_exc()
                    logger.exception(f"Failed to add view [{view}]")

        # send boot message
        # Send ready message
        if self.user is None:
            info = "cannot get my own infomation."
        else:
            info = f"Logged in as {self.user} (ID:{self.user.id})\nNow: {datetime.now(jst).strftime('%Y/%m/%d %H:%M:%S')}\nLibrary version: {discord.__version__}\nPython Info:{sys.version}"
        logger.info(info)


bot = MyBot()

if __name__ == "__main__":
    try:
        bot.run(token)
    except Exception:
        logger.exception("Failed to run MyBot")

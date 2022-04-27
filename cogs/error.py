from discord import ApplicationContext, DiscordException
from discord.ext import commands
from logger import getMyLogger
from now import get_now_str

logger = getMyLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_error")
    async def _on_error(self, event, something):
        now = get_now_str()
        msg = f"on_error:\n\n({now})\n{str(event)}\n\n{str(something)}"
        logger.error(msg)

    @commands.Cog.listener(name="on_command_error")
    async def _on_command_error(self, ctx: commands.Context, error):
        now = get_now_str()
        if isinstance(error, commands.MissingRole):
            await ctx.reply(content="このコマンドを実行する権限がありません。", mention_author=False)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply(content="指定されたコマンドは存在しません。", mention_author=False)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(content="Botに必要な権限がありません。", mention_author=False)
        else:
            await ctx.reply(content="不明なエラーが発生しました。", mention_author=False)
        logger.error(
            f"on_command_error:\n\n{now}\n{ctx.author}\n{ctx.command}\n\n{error}"
        )

    @commands.Cog.listener(name="on_application_command_error")
    async def _on_application_command_error(
        self, ctx: ApplicationContext, exception: DiscordException
    ):
        now = get_now_str()
        err = f"on_application_command_error:\n\n({now})\n\n{str(exception)}"
        await ctx.respond(
            content="エラーが発生しました。\n開発者に通知しましたので対応をお待ちください。", ephemeral=True
        )
        logger.error(err)


def setup(bot):
    return bot.add_cog(ErrorHandler(bot))

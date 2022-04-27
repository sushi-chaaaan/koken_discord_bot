import json
import os
import subprocess
from asyncio.log import logger

import discord
from discord.commands import slash_command
from discord.ext import commands
from dotenv import load_dotenv
from logger import getMyLogger

load_dotenv()

looger = getMyLogger(__name__)

guild_ids = [os.environ["GUILD_ID"], os.environ["TEST_GUILD_ID"]]


class MDPDF(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="markdown-pdf", guild_ids=guild_ids)
    async def markdown_pdf(
        self,
        ctx: discord.ApplicationContext,
        attachment: discord.Option(
            discord.Attachment,
            "変換するmarkdownファイル",
            required=True,
        ),
    ):
        """MarkdownファイルをPDFに変換します。"""
        await ctx.interaction.response.defer(ephemeral=True)

        # return if filetype is not markdown
        if not attachment.filename.endswith(".md"):
            await ctx.respond(
                content="MarkDown形式ではないファイルが添付されました。",
                ephemeral=True,
            )
            return

        # convert markdown to pdf
        await attachment.save(f"./tmp/{attachment.filename}")
        pure_name = attachment.filename.removesuffix(".md")
        result = self.md2html_md_to_pdf(f"./tmp/{attachment.filename}")

        # response (failed)
        if not result:
            await ctx.respond(
                content="実行に失敗しました",
                ephemeral=True,
            )
            return

        # response (success)
        try:
            await ctx.respond(
                content="pdfファイルへの変換に成功しました。",
                file=discord.File(result),
                ephemeral=True,
            )
        except Exception:
            logger.exception(f"Failed to send file [{result}]")
        finally:
            files = [f"./tmp/{attachment.filename}", result]
            for f in files:
                self.delete_file(f)

    def delete_file(self, filename: str):
        try:
            os.remove(filename)
        except Exception:
            logger.exception(f"Failed to delete file [{filename}]")

    def md2html_md_to_pdf(self, filename: str) -> str | None:
        pure_name = filename.removesuffix(".md")
        marked_opt = '{"gfm": true}'
        marked_json = json.dumps(marked_opt)
        pdf_opt = '{"format": "A4", "margin": "15mm", "printBackground": true}'
        pdt_json = json.dumps(pdf_opt)
        launch_opt = '{"args": ["--no-sandbox","--disable-setuid-sandbox"],"executablePath": "/usr/bin/google-chrome-stable"}'
        launch_json = json.dumps(launch_opt)
        try:
            subprocess.run(
                f"npx md-to-pdf --stylesheet styles/github-markdown.css --highlight-style github --marked-options {marked_json} --launch-options {launch_json} --pdf-options {pdt_json} {filename}",
                shell=True,
            )
        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to comp command [{e.cmd}]")
            return None
        else:
            return f"{pure_name}.pdf"


def setup(bot):
    return bot.add_cog(MDPDF(bot))

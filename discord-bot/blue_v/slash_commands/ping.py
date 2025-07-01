import discord
from discord.ext import commands
from discord import app_commands
import logging
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)


intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)


class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Check bot latency.')
    async def ping(self, interaction: discord.Interaction):

        latency = bot.latency  # Returns latency in seconds
        await interaction.response.send_message(f'Pong! Latency: {latency * 1000:.2f}ms')



async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))
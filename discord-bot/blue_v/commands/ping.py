import discord
from discord.ext import commands
import logging


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)


intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)


@bot.command(name='ping')
async def ping(ctx: commands.Context):
    latency = bot.latency  
    await ctx.send(f'🏓 Pong! Latency: {latency * 1000:.2f}ms')

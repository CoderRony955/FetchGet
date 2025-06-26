import discord
from discord.ext import commands
import asyncio
from commands.delete_req import DELETE
from commands.get_req import GET
from commands.patch_req import PATCH
from commands.put_req import PUT
from commands.post_req import POST
from dotenv import load_dotenv
import logging
import os


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)


@bot.event
async def on_ready():
    Activity = discord.Game(name='/help')
    await bot.change_presence(status=discord.Status.online, activity=Activity)
    logger.info(f'Bot {bot.user.name} has connected to Discord!')
    await bot.tree.sync()

# syncing all commands
bot.add_command(GET)
bot.add_command(POST)
bot.add_command(PUT)
bot.add_command(PATCH)
bot.add_command(DELETE)


async def load_commands():
    command_dir = os.path.join(os.path.dirname(__file__), "slash_commands")
    for filename in os.listdir(command_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            ext = f"slash_commands.{filename[:-3]}"
            print(f"Loading: {ext}")
            logger.info(f"Loading: {ext}")
            await bot.load_extension(ext)

bot_token = os.getenv('DISCORD_BOT_B')


async def main():
    await load_commands()
    await bot.start(bot_token)

asyncio.run(main())

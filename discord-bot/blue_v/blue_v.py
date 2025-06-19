import discord
from discord.ext import commands
import slash_cmds
from dotenv import load_dotenv
import logging
import os
import normal_cmds


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


bot.add_command(normal_cmds.GET)
bot.add_command(normal_cmds.POST)
bot.add_command(normal_cmds.PUT)
bot.add_command(normal_cmds.PATCH)
bot.add_command(normal_cmds.DELETE)

slash_cmds.setup(bot)

bot_token = os.getenv('DISCORD_BOT_B')
bot.run(bot_token)

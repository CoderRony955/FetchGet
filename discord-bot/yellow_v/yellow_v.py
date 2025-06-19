import discord
from discord.ext import commands
import slash_commands
from dotenv import load_dotenv
import logging
import os
import normal_commands


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


@bot.event
async def on_ready():
    Activity = discord.Game(name='/help')
    await bot.change_presence(status=discord.Status.online, activity=Activity)
    logger.info(f'Bot {bot.user.name} has connected to Discord!')
    await bot.tree.sync()


bot.add_command(normal_commands.GET)
bot.add_command(normal_commands.POST)
bot.add_command(normal_commands.PUT)
bot.add_command(normal_commands.PATCH)
bot.add_command(normal_commands.DELETE)
bot.add_command(normal_commands.whois_lookup)
bot.add_command(normal_commands.host_lookup)
bot.add_command(normal_commands.verify_url)
bot.add_command(normal_commands.ip_info)
bot.add_command(normal_commands.check_abusive_ip)
    

slash_commands.setup(bot)

bot_token = os.getenv('DISCORD_BOT_Y')
bot.run(bot_token)

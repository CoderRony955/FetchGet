import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)

load_dotenv()


@bot.command(name='ipinfo')
async def ip_info(ctx: commands.Context, ip: str):
    user = ctx.author
    try:
        async with httpx.AsyncClient() as client:
            get = await client.get(f'https://ipinfo.io/{ip}/json')
            embed = discord.Embed(
                title=f"Target IP: {ip}",
                description=get.text,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error {e}")
        embed = discord.Embed(
            title="Error ;-;",
            description=str(e),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)
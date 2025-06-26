import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)

load_dotenv()


@bot.command(name='get')
async def GET(ctx: commands.Context, url: str):
    try:
        user = ctx.author
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url)
            if response.status_code != 200:
                embed = discord.Embed(
                    title='Oops!',
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.green()

                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await ctx.send(embed=embed)
    except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
        logger.error(f"HTTP GET Request failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

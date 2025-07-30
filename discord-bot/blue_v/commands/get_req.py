import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
from dotenv import load_dotenv
import re
from urllib.parse import urlparse


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

        IP_REGEX = re.compile(
            r"(?:\d{1,3}\.){3}\d{1,3}"         # IPv4
            r"|"
            # IPv6 in brackets like [2001:db8::1]
            r"\[[0-9a-fA-F:]+\]"
        )

        def is_valid_url(URL: str) -> bool:
            path = urlparse(url).path  # Get the URL path part
            # Check if an IP address appears in the path
            if IP_REGEX.search(path):
                return True
            return False

        blockedurls = [
            "http://ip-api.com/json",
            "https://ipapi.co/json/",
            "https://ipapi.co/{IP}/json/",
            "https://freeipapi.com/json/",
            "http://ipwho.is/",
            "https://api.hackertarget.com/geoip/?q={IP}",
            "https://api.country.is/{IP}",
            "https://get.geojs.io/v1/ip/geo.json"
        ]

        for urls in blockedurls:
            if url in blockedurls or is_valid_url(URL=urls):
                embed = discord.Embed(
                    title='Uhh ⚠️',
                    description=f'URL {url} is not allowed to make request via **FetchGet Bot** for some security reasons!',
                    color=discord.Color.yellow()
                )

                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
                return

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

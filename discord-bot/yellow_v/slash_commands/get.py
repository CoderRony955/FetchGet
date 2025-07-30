import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import httpx
from dotenv import load_dotenv
import re
from urllib.parse import urlparse

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


class GetCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='get', description='Make a GET request to a valid URL')
    async def get(self, interaction: discord.Interaction, url: str):
        user = interaction.user
        try:
            await interaction.response.defer()
            
            IP_REGEX = re.compile(
                r"(?:\d{1,3}\.){3}\d{1,3}"         # IPv4
                r"|"
                r"\[[0-9a-fA-F:]+\]"               # IPv6 in brackets like [2001:db8::1]
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

                    await interaction.followup.send(embed=embed)
                    return

            async with httpx.AsyncClient() as client:
                response = await client.get(url=url)
                status = response.status_code
                text = response.text[:1900]  # Discord max message length

                embed = discord.Embed(
                    title='Response',
                    description=f'**Status**: {status}\n**Response**:\n{text}',
                    color=discord.Color.green() if status == 200 else discord.Color.red()
                )
                embed.set_footer(
                    text=f"Requested by {user.name}",
                    icon_url=user.avatar.url if user.avatar else user.default_avatar.url
                )
                await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"HTTP GET Request failed: {e}")
            embed = discord.Embed(
                title="Error",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(
                text=f"Requested by {user.name}",
                icon_url=user.avatar.url if user.avatar else user.default_avatar.url
            )
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(GetCog(bot))

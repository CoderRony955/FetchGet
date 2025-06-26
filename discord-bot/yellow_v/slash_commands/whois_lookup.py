import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import whois
from datetime import datetime
from dotenv import load_dotenv

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


class WhoisLookupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='whois', description='Use this command to perform WHOIS lookup on any particular valid domain.')
    async def whois_lookup(self, interaction: discord.Interaction, domain: str):

        try:
            user = interaction.user
            await interaction.response.defer()
            info = whois.whois(domain)

            def format_value(value):
                if isinstance(value, list):
                    return ', '.join(str(format_value(v)) for v in value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                return str(value)

            embed = discord.Embed(
                title=f"WHOIS lookup for `{domain}`",
                color=discord.Color.blue()
            )

            for key, value in info.items():
                if value:
                    formatted = format_value(value)
                    if len(formatted) > 1024:
                        formatted = formatted[:1020] + '...'
                    embed.add_field(name=key, value=formatted, inline=False)
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Error during WHOIS lookup: {e}")
            embed = discord.Embed(
                title="Error during WHOIS lookup",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(WhoisLookupCog(bot))

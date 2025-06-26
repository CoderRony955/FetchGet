import discord
from discord.ext import commands
from discord import app_commands
import logging
import httpx

logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


class IpLookupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='ipinfo', description='Get information of any valid IP address.')
    async def ip_info(self, interaction: discord.Interaction, ip: str):
        user = interaction.user
        try:
            await interaction.response.defer()
            async with httpx.AsyncClient() as client:
                get = await client.get(f'https://ipinfo.io/{ip}/json')
                embed = discord.Embed(
                    title=f"Target IP: {ip}",
                    description=get.text,
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Error {e}")
            embed = discord.Embed(
                title="Error ;-;",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(IpLookupCog(bot))

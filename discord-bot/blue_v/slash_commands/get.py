import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import httpx
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



class GetCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='get', description='Make a GET request to a valid URL')
    async def get(self, interaction: discord.Interaction, url: str):
        user = interaction.user
        try:
            await interaction.response.defer()
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

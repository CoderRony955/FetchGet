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




class PostCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='post', description='Make a POST request with up to 5 key-value pairs.')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def post(self,
        interaction: discord.Interaction,
        url: str,
        k1: str, v1: str,
        k2: str = None, v2: str = None,
        k3: str = None, v3: str = None,
        k4: str = None, v4: str = None,
        k5: str = None, v5: str = None,
    ):
        user = interaction.user
        await interaction.response.defer()
        data = {
            k: v for k, v in [(k1, v1), (k2, v2), (k3, v3), (k4, v4), (k5, v5)] if k is not None
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=data)

            embed_color = discord.Color.green(
            ) if response.status_code == 200 else discord.Color.red()
            embed = discord.Embed(
                title='POST Request Result',
                description=f'**Status**: {response.status_code}\n**Response**: {response.text[:1900]}',
                color=embed_color
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"HTTP POST Request failed: {e}")
            embed = discord.Embed(
                title="Error",
                description=f'**Exception**: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(PostCog(bot))

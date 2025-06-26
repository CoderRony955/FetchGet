import discord
from discord.ext import commands
from discord import app_commands
import logging
import json
import httpx


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)


intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


class DelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='delete', description='Make DELETE requests by using valid URL.')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def delete(self,
        interaction: discord.Interaction,
        url: str,
        k1: str = None, v1: str = None,
        k2: str = None, v2: str = None,
        k3: str = None, v3: str = None,
        k4: str = None, v4: str = None,
        k5: str = None, v5: str = None,
    ):
        user = interaction.user
        await interaction.response.defer()
        try:
            data = {
                k: v for k, v in [(k1, v1), (k2, v2), (k3, v3), (k4, v4), (k5, v5)] if k is not None
            }

            headers = {'Content-Type': 'application/json'}

            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method="DELETE",
                    url=url,
                    headers=headers,
                    content=json.dumps(data)  # Manually serialize the data
                )

            # Embed for feedback
            embed = discord.Embed(
                title='Response',
                description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                color=discord.Color.green() if response.status_code == 200 else discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

        except (httpx.RequestError, Exception) as e:
            logger.error(f"HTTP DELETE failed: {e}")
            embed = discord.Embed(
                description=f'**Error**: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DelCog(bot))

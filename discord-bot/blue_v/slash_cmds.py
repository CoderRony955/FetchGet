import discord
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
import logging
import httpx
import json
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)


@bot.event
async def on_ready():
    Activity = discord.Game(name='/help')
    await bot.change_presence(status=discord.Status.online, activity=Activity)
    logger.info(f'Bot {bot.user.name} has connected to Discord!')
    await bot.tree.sync()


def setup(bot: commands.Bot):

    @bot.tree.command(name='get', description='make get requests by using valid URL')
    async def get(interaction: discord.Interaction, url: str):
        user = interaction.user
        try:
            await interaction.response.defer()  # optional, for longer requests
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url)
                if response.status_code != 200:
                    embed = discord.Embed(
                        title='Oops!',
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.red()
                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.green()

                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)
        except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
            logger.error(f"HTTP GET Request failed: {e}")
            embed = discord.Embed(
                description=f'**Error**: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

    # -----------------------------------------------------------------

    @bot.tree.command(name='post', description='Make a POST request with up to 5 key-value pairs.')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def post(
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

    # -----------------------------------------------------------------

    @bot.tree.command(name='put', description='make PUT requests by using valid URL and providing data to send via PUT request')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def put(
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
        try:
            data = {
                k1: v1,
                k2: v2,
                k3: v3,
                k4: v4,
                k5: v5
            }
            async with httpx.AsyncClient() as client:
                response = await client.put(url=url, data=data)
                if response.status_code != 200:
                    embed = discord.Embed(
                        title='Oops!',
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.red()
                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.green()

                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)
        except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
            logger.error(f"HTTP PUT Request failed: {e}")
            embed = discord.Embed(
                description=f'**Error**: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

    # -----------------------------------------------------------------

    @bot.tree.command(name='patch', description='make PATCH requests by using valid URL and providing data to send via PATCH request')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def patch(
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
        try:
            data = {
                k1: v1,
                k2: v2,
                k3: v3,
                k4: v4,
                k5: v5
            }
            async with httpx.AsyncClient() as client:
                response = await client.patch(url=url, data=data)
                if response.status_code != 200:
                    embed = discord.Embed(
                        title='Oops!',
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.red()
                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                        color=discord.Color.green()

                    )
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)
        except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
            logger.error(f"HTTP PUT Request failed: {e}")
            embed = discord.Embed(
                description=f'**Error**: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

    # -----------------------------------------------------------------

    @bot.tree.command(name='delete', description='make DELETE requests by using valid URL')
    @app_commands.describe(
        url="The endpoint URL",
        k1="Key 1", v1="Value 1",
        k2="Key 2", v2="Value 2",
        k3="Key 3", v3="Value 3",
        k4="Key 4", v4="Value 4",
        k5="Key 5", v5="Value 5",
    )
    async def delete(
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

    # -----------------------------------------------------------------

    @bot.tree.command(name='help', description='See all available commands')
    async def help(interaction: discord.Interaction):
        try:
            help_des = """
            **FetchGet B1.0** here to help you to perform some basics networking tasks. 
            
            Here is the available commands:
            
            `/get {url}`: Make GET requests
        
            `/post {url} k1 data v1 data` **8 more optional key and value pairs available to send data via POST requests**: Make POST requests by using valid URL and providing data to send via POST request
            
            `/put {url} k1 data v1 data` **8 more optional key and value pairs available to send data via PUT requests**: Make PUT requests by using valid URL and providing data to send via PUT request
            
            `/patch {url} k1 data v1 data` **8 more optional key and value pairs available to send data via PATCH requests**: Make PATCH requests by using valid URL and providing data to send via PATCH request
            
            `/delete {url}` **10 optional key and value pairs available to send payloads via DELETE requests**: Make DELETE requests by using valid URL and providing payload if required to send via DELETE request
            
            
            **One more thing by the way my default perfix is `,` if you want to perfer use commands using my perfix then you can use it.**
            
            
            """

            bot_avatar_url = bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url
            embed = discord.Embed(
                title="AsciiAce bot help",
                description=help_des,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=bot_avatar_url)
            embed.set_footer(text=f"{bot.user.name}", icon_url=bot_avatar_url)
            await interaction.response.send_message(embed=embed)

        except discord.DiscordException as e:
            logger.error(f'An Exception error occurred: {e}')
            embed = discord.Embed(
                title='Oops!',
                description=f'An Exception error occurred: {e}',
                color=discord.Color.red()
            )
            logger.error(f'An exception error occurred: {e}')
            await interaction.response.send_message(embed=embed)

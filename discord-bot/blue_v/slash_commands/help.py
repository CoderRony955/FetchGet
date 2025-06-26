import discord
from discord.ext import commands
from discord import app_commands
import logging


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='help', description='See all available commands.')
    async def help(self, interaction: discord.Interaction):
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
                title="FetchGet B1.0 help",
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


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))

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
            What is going on **Networking guy**? **FetchGet Y1.1** here to help you to perform some Networking related tasks. But what kind of networking related tasks? Hold on hold on.. bro let me tell you. Let's see all available commands that perform each and unqiue task, see given below:
            
            
            **Want to make HTTP requests?**
            Use these commands:
            
            `/get {url}`: Make GET requests
            
            `/post {url} k1 data v1 data` **8 more optional key and value pairs available to send data via POST requests**: Make POST requests by using valid URL and providing data to send via POST request
            
            `/put {url} k1 data v1 data` **8 more optional key and value pairs available to send data via PUT requests**: Make PUT requests by using valid URL and providing data to send via PUT request
            
            `/patch {url} k1 data v1 data` **8 more optional key and value pairs available to send data via PATCH requests**: Make PATCH requests by using valid URL and providing data to send via PATCH request
            
            `/delete {url}` **10 optional key and value pairs available to send payloads via DELETE requests**: Make DELETE requests by using valid URL and providing payload if required to send via DELETE request
            
            **Other commands**:
            
            `/whois {target domain}`: Use this command to perform WHOIS lookup on any particular valid domain
            
            `/dlookup {target domain}`: Use this command to perform dnslookup on any particular valid domain
            
            `/ipinfo {target ip}`: Get information of any valid IP address
            
            `/verify {target domain or url}`: Check url, domain if it is suspicious or not
            
            `/abuseip {target ip}`: Check any IP if it is abusive or not **(abusive means if any IP is responsible to perform malicious taks on the internet then that IP is abusive)**
            
            `/find {target username}`: Perform username lookup on over 20+ social networks to find user
            
            `/publicdns`: Get a list of public DNS servers
            
            
            **One more thing by the way my default perfix is `;` if you want to perfer use commands using my perfix then you can use it.**
            
            
            """

            # Safely get the bot's avatar
            bot_user = self.bot.user
            if bot_user.avatar:
                bot_avatar_url = bot_user.avatar.url
            else:
                bot_avatar_url = bot_user.default_avatar.url

            embed = discord.Embed(
                title="FetchGet Y1.1 Help",
                description=help_des,
                color=discord.Color.yellow()
            )
            embed.set_thumbnail(url=bot_avatar_url)
            embed.set_footer(text=bot_user.name, icon_url=bot_avatar_url)

            await interaction.response.send_message(embed=embed)

        except discord.DiscordException as e:
            embed = discord.Embed(
                title='Oops!',
                description=f'An error occurred: {e}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

# Register the cog


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))

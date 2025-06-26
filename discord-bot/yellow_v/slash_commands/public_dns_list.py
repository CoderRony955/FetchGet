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


class DnsListCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='publicdns', description='Get the list of public DNS servers.')
    async def dns_list(self, interaction: discord.Interaction):
        user = interaction.user
        try:
            public_dns_list = """1. [Cloudflare DNS](https://one.one.one.one/): `1.1.1.1`
2. [Google DNS](https://developers.google.com/speed/public-dns/): `8.8.8.8`
3. [Quad9](https://quad9.net/): `9.9.9.9`
4. [OpenDNS (Cisco)](https://www.opendns.com/): `208.67.222.222`
5. [CleanBrowsing](https://cleanbrowsing.org/): `185.228.168.9`
6. [AdGuard DNS](https://adguard-dns.io/en/welcome.html): `94.140.14.14`
7. [DNS.SB](https://dns.sb/): `185.222.222.222`
8. [Alternate DNS](https://alternate-dns.com/): `76.76.19.19`
9. [Verisign Public DNS](https://www.publicdns.xyz/public/verisign.html): `64.6.64.6`
10. [Comodo Secure DNS](https://www.comodo.com/secure-dns/): `8.26.56.26`"""

            embed = discord.Embed(
                title="Here is the list of all public DNS servers:",
                description=public_dns_list,
                color=discord.Color.blue()
            )
            embed.set_footer(
                text=f"Requested by {user.name}",
                icon_url=user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            logger.error(f"Error: {e}")
            embed = discord.Embed(
                title="Error",
                description=f'Error while giving response',
                color=discord.Color.red()
            )
            embed.set_footer(
                text=f"Requested by {user.name}",
                icon_url=user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DnsListCog(bot))

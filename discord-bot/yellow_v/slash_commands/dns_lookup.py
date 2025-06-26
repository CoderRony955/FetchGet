import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import dns.resolver
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




class DnsLookupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='dlookup', description='Use this command to perform dnslookup on any particular valid domain.')
    async def host_lookup(self, interaction: discord.Interaction, domain: str):
        user = interaction.user
        await interaction.response.defer()
        record_types = [
            "A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA",
            "SRV", "CAA", "DNSKEY", "DS", "RRSIG", "TLSA",
            "NAPTR", "SPF"
        ]
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["1.1.1.1", "8.8.8.8"]
        resolver.lifetime = 5

        embed = discord.Embed(
            title=f"DNS Lookup for `{domain}`",
            color=discord.Color.blue()
        )

        for record_type in record_types:
            try:
                answers = resolver.resolve(domain, record_type)
                records = [r.to_text() for r in answers]
                result = '\n'.join(records)

                # Truncate if too long (Discord limit per field = 1024 chars)
                if len(result) > 1024:
                    result = result[:1020] + '...'

                embed.add_field(name=record_type, value=result, inline=False)

            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
                continue

        if not embed.fields:
            embed.description = "No DNS records found or the domain is invalid."
            embed.color = discord.Color.red()
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DnsLookupCog(bot))

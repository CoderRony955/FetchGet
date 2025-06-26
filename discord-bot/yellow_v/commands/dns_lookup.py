import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import dns.resolver
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)

load_dotenv()


@bot.command(name='dlookup')
async def host_lookup(ctx: commands.Context, domain: str):
    user = ctx.author

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
    await ctx.send(embed=embed)

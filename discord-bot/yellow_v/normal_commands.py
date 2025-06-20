import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
import json
import whois
import vt
import os
import json
import time
from dotenv import load_dotenv
import dns.resolver
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    filename="fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)

load_dotenv()


@bot.command(name='get')
async def GET(ctx: commands.Context, url: str):
    try:
        user = ctx.author
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url)
            if response.status_code != 200:
                embed = discord.Embed(
                    title='Oops!',
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.green()

                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await ctx.send(embed=embed)
    except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
        logger.error(f"HTTP GET Request failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='post')
async def POST(
    ctx: commands.Context,
    url: str,
    k1: str, v1: any,
    k2: str = None, v2: any = None,
    k3: str = None, v3: any = None,
    k4: str = None, v4: any = None,
    k5: str = None, v5: any = None,
):
    user = ctx.author
    try:
        data = {
            k1: v1,
            k2: v2,
            k3: v3,
            k4: v4,
            k5: v5
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, data=data)
            if response.status_code != 200:
                embed = discord.Embed(
                    title='Oops!',
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.green()

                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await ctx.send(embed=embed)
    except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
        logger.error(f"HTTP POST Request failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='put')
async def PUT(
    ctx: commands.Context,
    url: str,
    k1: str, v1: any,
    k2: str = None, v2: any = None,
    k3: str = None, v3: any = None,
    k4: str = None, v4: any = None,
    k5: str = None, v5: any = None,
):
    user = ctx.author
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
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.green()

                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await ctx.send(embed=embed)
    except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
        logger.error(f"HTTP PUT Request failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='patch')
async def PATCH(
    ctx: commands.Context,
    url: str,
    k1: str, v1: any,
    k2: str = None, v2: any = None,
    k3: str = None, v3: any = None,
    k4: str = None, v4: any = None,
    k5: str = None, v5: any = None,
):
    user = ctx.author
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
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f'**Response**: {response.text}\n\n**Status**: {response.status_code}',
                    color=discord.Color.green()

                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await ctx.send(embed=embed)
    except (httpx.ProxyError, httpx.NetworkError, httpx.RequestError, httpx.TimeoutException, Exception) as e:
        logger.error(f"HTTP PUT Request failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='delete')
async def DELETE(
    ctx: commands.Context,
    url: str,
    k1: str = None, v1: any = None,
    k2: str = None, v2: any = None,
    k3: str = None, v3: any = None,
    k4: str = None, v4: any = None,
    k5: str = None, v5: any = None
):
    user = ctx.author
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
            description=f'**Status**: {response.status_code}\n\n**Response**: {response.text}',
            color=discord.Color.green() if response.status_code == 200 else discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

        await ctx.send(embed=embed)

    except (httpx.RequestError, Exception) as e:
        logger.error(f"HTTP DELETE failed: {e}")
        embed = discord.Embed(
            description=f'**Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='whois')
async def whois_lookup(ctx: commands.Context, domain: str):
    user = ctx.author
    try:

        info = whois.whois(domain)

        def format_value(value):
            if isinstance(value, list):
                return ', '.join(str(format_value(v)) for v in value)
            elif isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            return str(value)

        embed = discord.Embed(
            title=f"WHOIS lookup for `{domain}`",
            color=discord.Color.blue()
        )

        for key, value in info.items():
            if value:
                formatted = format_value(value)
                if len(formatted) > 1024:
                    formatted = formatted[:1020] + '...'
                embed.add_field(name=key, value=formatted, inline=False)
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error during WHOIS lookup: {e}")
        error_embed = discord.Embed(
            title="Error during WHOIS lookup",
            description=str(e),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=error_embed)

# -----------------------------------------------------------------


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

# -----------------------------------------------------------------


@bot.command(name='verify')
async def verify_url(ctx: commands.Context, target: str):
    user = ctx.author
    try:
        api_key = os.getenv('VIRUSTOTAL_APIKEY')
        if not api_key:
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await ctx.send("VirusTotal API key not found in environment variables.")
            return

        def scan_and_fetch():
            with vt.Client(api_key) as client:
                analysis = client.scan_url(target)
                # Wait for analysis to complete
                while True:
                    analysis = client.get_object(f"/analyses/{analysis.id}")
                    if analysis.status == "completed":
                        break
                    time.sleep(2)

                url_id = vt.url_id(target)
                url_obj = client.get_object(f"/urls/{url_id}")
                return url_obj.get("last_analysis_stats", {})

        stats = await ctx.bot.loop.run_in_executor(None, scan_and_fetch)

        if not stats:
            embed = discord.Embed(
                title=f"Oops!",
                description="❌ No analysis stats found. Try scanning again later.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"🔍 Scan Summary for: {target}",
            description=(
                f"✅ **Harmless**: {stats.get('harmless', 0)}\n"
                f"⚠️ **Suspicious**: {stats.get('suspicious', 0)}\n"
                f"❌ **Malicious**: {stats.get('malicious', 0)}\n"
                f"🧐 **Undetected**: {stats.get('undetected', 0)}"
            ),
            color=discord.Color.green() if stats.get(
                'malicious', 0) == 0 else discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

        if stats.get('malicious', 0) > 0 or stats.get('suspicious', 0) > 0:
            logger.warning("⚠️ This URL may be phishing or malicious.")
        else:
            logger.info("✅ This URL appears clean.")

    except Exception as e:
        logger.error(f"Error {e}")
        embed = discord.Embed(
            title="Error ;-;",
            description=str(e),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='ipinfo')
async def ip_info(ctx: commands.Context, ip: str):
    user = ctx.author
    try:
        async with httpx.AsyncClient() as client:
            get = await client.get(f'https://ipinfo.io/{ip}/json')
            embed = discord.Embed(
                title=f"Target IP: {ip}",
                description=get.text,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error {e}")
        embed = discord.Embed(
            title="Error ;-;",
            description=str(e),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

# -----------------------------------------------------------------


@bot.command(name='abuseip')
async def check_abusive_ip(ctx: commands.Context, ip: str):
    api_key = os.getenv('ABUSE_IPDB_APIKEY')
    user = ctx.author

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()["data"]

                embed = discord.Embed(
                    title=f"AbuseIPDB Report for {ip}",
                    color=discord.Color.green()
                )

                embed.add_field(name="IP Address", value=data.get(
                    "ipAddress", "N/A"), inline=True)
                embed.add_field(
                    name="Abuse Score", value=f"{data.get('abuseConfidenceScore', 'N/A')}%", inline=True)
                embed.add_field(name="Country", value=data.get(
                    "countryCode", "N/A"), inline=True)
                embed.add_field(name="Domain", value=data.get(
                    "domain", 'N/A') or "None", inline=True)
                embed.add_field(name="Is Tor", value=data.get(
                    "isTor", 'N/A') or "None", inline=True)
                embed.add_field(name="ISP", value=data.get(
                    "isp", "N/A"), inline=False)
                embed.add_field(name="Total Reports", value=data.get(
                    "totalReports", "N/A"), inline=True)
                embed.add_field(name="Last Reported", value=data.get(
                    "lastReportedAt", "Never"), inline=True)

                embed.set_footer(
                    text=f"Requested by {user.name}",
                    icon_url=user.display_avatar.url
                )

                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Error fetching data from AbuseIPDB",
                    description=f'**Status**: {response.status_code}\n**Response**: {response.text}',
                    color=discord.Color.red()
                )
                embed.set_footer(
                    text=f"Requested by {user.name}",
                    icon_url=user.display_avatar.url
                )
                await ctx.send(embed=embed)

    except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, Exception) as e:
        logger.error(f"AbuseIPDB API error: {e}")
        embed = discord.Embed(
            title="Exception occurred",
            description=f'**Error**: {str(e)}',
            color=discord.Color.red()
        )
        embed.set_footer(
            text=f"Requested by {user.name}",
            icon_url=user.display_avatar.url
        )
        await ctx.send(embed=embed)

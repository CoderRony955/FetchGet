import discord
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
import logging
import httpx
import json
import whois
import vt
import os
import time
from dotenv import load_dotenv
import dns.resolver
from datetime import datetime


load_dotenv()

logging.basicConfig(level=logging.INFO,
                    filename="fetchget_y.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=';', intents=intents)


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

    @bot.tree.command(name='whois', description='use this command to perform WHOIS lookup on any particular valid domain')
    async def whois_lookup(interaction: discord.Interaction, domain: str):
        try:
            user = interaction.user
            await interaction.response.defer()
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
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Error during WHOIS lookup: {e}")
            embed = discord.Embed(
                title="Error during WHOIS lookup",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

    # -----------------------------------------------------------------

    @bot.tree.command(name='dlookup', description='use this command to perform dnslookup on any particular valid domain')
    async def host_lookup(interaction: discord.Interaction, domain: str):
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

    # -----------------------------------------------------------------

    @bot.tree.command(name='verify', description='check url, domain if it is suspicious or not')
    async def verify_url(interaction: discord.Interaction, target: str):
        user = interaction.user
        try:
            await interaction.response.defer()
            api_key = os.getenv('VIRUSTOTAL_APIKEY')
            if not api_key:
                await interaction.followup.send("VirusTotal API key not found in environment variables.")
                return

            def scan_and_fetch():
                with vt.Client(api_key) as client:
                    analysis = client.scan_url(target)
                    # Wait for analysis to complete
                    while True:
                        analysis = client.get_object(
                            f"/analyses/{analysis.id}")
                        if analysis.status == "completed":
                            break
                        time.sleep(2)

                    url_id = vt.url_id(target)
                    url_obj = client.get_object(f"/urls/{url_id}")
                    return url_obj.get("last_analysis_stats", {})

            # Run blocking code in thread executor
            stats = await interaction.client.loop.run_in_executor(None, scan_and_fetch)

            if not stats:
                embed = discord.Embed(
                    title=f"Oops!",
                    description="❌ No analysis stats found. Try scanning again later.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await interaction.followup.send(embed=embed)
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
            await interaction.followup.send(embed=embed)

            if stats.get('malicious', 0) > 0 or stats.get('suspicious', 0) > 0:
                logger.warning("⚠️ This URL may be phishing or malicious.")
            else:
                logger.info("✅ This URL appears clean.")

        except Exception as e:
            logger.error(f"Error during scan: {e}")
            embed = discord.Embed(
                title="🚨 Error during scan",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

    # -----------------------------------------------------------------

    @bot.tree.command(name='ipinfo', description='Get information of any valid IP address')
    async def ip_info(interaction: discord.Interaction, ip: str):
        user = interaction.user
        try:
            await interaction.response.defer()
            async with httpx.AsyncClient() as client:
                get = await client.get(f'https://ipinfo.io/{ip}/json')
                embed = discord.Embed(
                    title=f"Target IP: {ip}",
                    description=get.text,
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"Requested by {user.name}",
                                 icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Error {e}")
            embed = discord.Embed(
                title="Error ;-;",
                description=str(e),
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
            What is going on **Networking guy**? **FetchGet Y1.0** here to help you to perform some Networking related tasks. But what kind of networking related tasks? Hold on hold on.. bro let me tell you. Let's see all available commands that perform each and unqiue task, see given below:
            
            
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
            
            
            **One more thing by the way my default perfix is `;` if you want to perfer use commands using my perfix then you can use it.**
            
            
            """

            bot_avatar_url = bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url
            embed = discord.Embed(
                title="AsciiAce bot help",
                description=help_des,
                color=discord.Color.yellow()
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

    # -----------------------------------------------------------------

    @bot.tree.command(name='abuseip', description='Check any IP if it is abusive or not')
    async def check_abusive_ip(interaction: discord.Interaction, ip: str):
        api_key = os.getenv('ABUSE_IPDB_APIKEY')
        user = interaction.user

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
            await interaction.response.defer()
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

                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)

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
                    embed.set_footer(text=f"Requested by {user.name}",
                                     icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                    await interaction.followup.send(embed=embed)

        except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, Exception) as e:
            logger.error(f"Error {e}")
            embed = discord.Embed(
                title="Error ;-;",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {user.name}",
                             icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
            await interaction.followup.send(embed=embed)

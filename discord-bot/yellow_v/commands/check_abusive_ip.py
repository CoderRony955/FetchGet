import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
import os
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

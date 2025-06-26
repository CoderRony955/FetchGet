import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import whois
from dotenv import load_dotenv
from datetime import datetime

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

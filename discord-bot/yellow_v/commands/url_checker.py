import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import vt
import time
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

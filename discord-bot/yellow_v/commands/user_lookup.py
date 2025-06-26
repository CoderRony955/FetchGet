import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
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


@bot.command(name='find')
async def find_user(ctx: commands.Context, username: str):
    user = ctx.author
    social_platforms = {
        'Instagram': f'https://www.instagram.com/{username}',
        'Telegram': f'https://t.me/{username}',
        'X (Twitter)': f'https://x.com/{username}',
        'Threads': f'https://www.threads.net/@{username}',
        'YouTube': f'https://www.youtube.com/@{username}',
        'GitHub': f'https://github.com/{username}',
        'Reddit': f'https://www.reddit.com/user/{username}',
        'Twitch': f'https://www.twitch.tv/{username}',
        'Pinterest': f'https://in.pinterest.com/{username}/',
        'Facebook': f'https://www.facebook.com/{username}',
        'LinkedIn': f'https://www.linkedin.com/in/{username}',
        'Medium': f'https://medium.com/@{username}',
        'HuggingFace': f'https://huggingface.co/{username}',
        'Kaggle': f'https://www.kaggle.com/{username}',
        'Bluesky': f'https://bsky.app/profile/{username}.bsky.social',
        'SoundCloud': f'https://soundcloud.com/{username}',
        'Dev.to': f'https://dev.to/{username}',
        'Product Hunt': f'https://www.producthunt.com/@{username}',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'Behance': f'https://www.behance.net/{username}',
        'Dribbble': f'https://dribbble.com/{username}',
        'Replit': f'https://replit.com/@{username}',
        'Steam': f'https://steamcommunity.com/id/{username}',
        'BuyMeACoffee': f'https://www.buymeacoffee.com/{username}',
        'Patreon': f'https://www.patreon.com/{username}',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +https://example.com/bot)"
    }

    results = []

    try:
        async with httpx.AsyncClient(timeout=10, headers=headers, follow_redirects=True) as client:
            for platform, url in social_platforms.items():
                try:
                    response = await client.get(url)

                    # Basic not found detection
                    if platform == "Instagram" and ("Page Not Found" in response.text or response.status_code == 404):
                        results.append(f"❌ **{platform}**: Not Found")
                    elif platform == "GitHub" and ("Not Found" in response.text or response.status_code == 404):
                        results.append(f"❌ **{platform}**: Not Found")
                    elif response.status_code in [404, 410]:
                        results.append(f"❌ **{platform}**: Not Found")
                    else:
                        results.append(
                            f"✅ **{platform}**: [View Profile]({url})")

                except httpx.RequestError as e:
                    results.append(
                        f"⚠️ **{platform}**: Request Error - `{str(e)}`")
                except Exception as e:
                    results.append(
                        f"⚠️ **{platform}**: Unexpected Error - `{str(e)}`")

        # Build and send the final embed
        embed = discord.Embed(
            title=f"🔎 Social Links for `{username}`",
            description="\n".join(results),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        embed = discord.Embed(
            description=f'❌ **Fatal Error**: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

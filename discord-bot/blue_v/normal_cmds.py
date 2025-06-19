import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import httpx
import json
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO,
                    filename="log/discord_bots/discord_fetchget_b.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix=',', intents=intents)

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



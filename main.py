import json
import os
from datetime import datetime
import psutil

import discord
from discord.ext import commands
from dotenv import load_dotenv
from logpy import Logger
from logpy.ansi import BackgroundColor, Effect, ForegroundColor
from logpy.log import Format, Level
import asyncio
from pretty_help import PrettyHelp, AppMenu

start_time = datetime.now()

custom_format = Format("$date $time $level     $message", "%Y-%m-%d", "%H:%M:%S")
logger = Logger(custom_format)
info = Level(
    "INFO",
    ForegroundColor.green,
    BackgroundColor.black,
    Effect.bold
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

menu = AppMenu()

help_command = PrettyHelp(menu=menu, no_category="Extra")

# get owners
def get_owners():
    with open("owners.json", "r") as f:
        owners = json.load(f)

    return owners

def get_prefix(bot, message):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)

    return prefix.get(str(message.guild.id), "owl.")

bot = commands.Bot(
    command_prefix=get_prefix, help_command=help_command, intents=intents, owner_ids=get_owners()
)

@bot.event
async def on_ready():
    logger.log(f"{bot.user.name} is alive!", info)

@bot.hybrid_command(help="ping the bot")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong!\n{round(bot.latency * 1000)}ms")

@bot.hybrid_command(help="get bot info")
async def stats(ctx):
    try:
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process().memory_full_info().uss / 1024**2
        )
    except AttributeError:
        # OS doesn't support retrieval of USS (probably BSD or Solaris)
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process().memory_full_info().rss / 1024**2
        )
    sysboot = datetime.fromtimestamp(psutil.boot_time()).strftime(
        "%B %d, %Y at %I:%M:%S %p"
    )
    uptime = datetime.now() - start_time
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    days, hours = divmod(hours, 24)
    guilds = ctx.bot.guilds

    if days:
        time = "%s days, %s hours, %s minutes, and %s seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    else:
        time = "%s hours, %s minutes, and %s seconds" % (hours, minutes, seconds)
    em = discord.Embed(title="System Status", color=0x32441C)
    em.add_field(
        name=":gear: Library Version",
        value=f"discord.py {discord.__version__}",
        inline=False,
    )
    em.add_field(name="\U0001F4BE BOT Memory usage", value=mem_usage, inline=False)
    em.add_field(name="\U0001F553 BOT Uptime", value=time, inline=False)
    em.add_field(name="⏲️ Last System Boot Time", value=sysboot, inline=False)
    em.add_field(name="🛰️ Servers (Guilds)", value=str(len(guilds)), inline=False)
    await ctx.send(embed=em)

@bot.hybrid_command(help="get invite link")
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Link",
        url="https://discord.com/api/oauth2/authorize?client_id=875328150165413918&permissions=8&scope=bot",
        description="Invite the bot to your server",
        color=discord.Color.green(),
    )
    embed.set_footer(text="<3")
    await ctx.send(embed=embed)

@bot.hybrid_command(help="get support server link")
async def support(ctx):
    embed = discord.Embed(
        title="Support Server",
        url="https://discord.gg/DxyUU85Ca9",
        description="Join the support server for help and updates",
        color=discord.Color.green()
    )
    embed.set_footer(text="<3")
    await ctx.send(embed=embed)

@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def bot_in(ctx):
    guilds = ctx.bot.guilds
    list = []
    for guild in guilds:
        list.append(f"{guild.name}: {guild.id}")
        
    await ctx.send("```" + "\n".join(list) + "```")

# cogs
async def cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.log(f"Loaded cog {filename[:-3]}", info)
        
    await bot.load_extension("jishaku")

@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")

@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}")

@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension}")

async def main():
    load_dotenv()
    await cogs()
    await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

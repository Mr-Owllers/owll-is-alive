import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from logpy import Logger
from logpy.ansi import BackgroundColor, Effect, ForegroundColor
from logpy.log import Format, Level
import asyncio

custom_format = Format("$date $time $level     $message", "%Y-%m-%d", "%H:%M:%S")
logger = Logger(custom_format)
info = Level(
    "INFO",
    ForegroundColor.green,
    BackgroundColor.black,
    Effect.bold
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

help_command = commands.DefaultHelpCommand(no_category="Other Commands")

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
    command_prefix=get_prefix, help_command=help_command, intents=intents
)

bot.owners = get_owners()

@bot.event
async def on_ready():
    logger.log(f"{bot.user.name} is alive!", info)

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong!\n{round(bot.latency * 1000)}ms")

# cogs
async def cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.log(f"Loaded cog {filename[:-3]}", info)

@bot.hybrid_command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")

@bot.hybrid_command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}")

@bot.hybrid_command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension}")

async def main():
    await cogs()
    await bot.start(os.getenv("TOKEN"))
    
if __name__ == "__main__":
    asyncio.run(main())

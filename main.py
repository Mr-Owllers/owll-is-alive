import json
import os

import hikari
import lightbulb
from dotenv import load_dotenv
from logpy import Logger
from logpy.ansi import BackgroundColor, Effect, ForegroundColor
from logpy.log import Format, Level

custom_format = Format(
    "[$date $time $level logger] $message",
    "%Y-%m-%d",
    "%H:%M:%S"
)
logger = Logger(custom_format)
info = Level(
    "INFO",
    ForegroundColor.green,
    BackgroundColor.black,
    Effect.bold
)

load_dotenv()

def get_prefix(_client, ctx: lightbulb.Context):
    """get prefix function"""
    with open("prefix.json", "r", encoding="utf-8") as file:
        prefixes = json.load(file)

    guild_id = str(ctx.guild_id)
    if guild_id in prefixes:
        prfx = prefixes[guild_id]
    else:
        prfx = "owl."  # Prefix defaults to this if none is set for the server
    return prfx

client = lightbulb.BotApp(
    prefix=get_prefix,
    token=os.getenv("TOKEN"),
    intents=hikari.Intents.ALL,
    help_slash_command=True
)

with open("owners.json", "r", encoding="utf-8") as file:
    owners = json.load(file)

@lightbulb.Check
def is_owner(ctx) -> bool:
    return ctx.author.id in owners

@client.listen(hikari.ShardReadyEvent)
async def ready_listener(_):
    logger.log("owll is alive!", info) #hello

# extension stuff

client.load_extensions_from("./extensions")

@client.command
@lightbulb.add_checks(is_owner)
@lightbulb.option("ext_name", "which ext u wanna load?")
@lightbulb.command("load", "loads an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def load(ctx):
    ext = ctx.options.ext_name
    client.load_extensions(f"extensions.{ext}")
    await ctx.respond(f"{ext} loaded!")

@client.command
@lightbulb.add_checks(is_owner)
@lightbulb.option("ext_name", "which ext u wanna unload?")
@lightbulb.command("unload", "unloads an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def unload(ctx):
    ext = ctx.options.ext_name
    client.unload_extensions(f"extensions.{ext}")
    await ctx.respond(f"{ext} unloaded!")

@client.command
@lightbulb.add_checks(is_owner)
@lightbulb.option("ext_name", "which ext u wanna reload?")
@lightbulb.command("reload", "reloads an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def reload(ctx):
    ext = ctx.options.ext_name
    client.reload_extensions(f"extensions.{ext}")
    await ctx.respond(f"{ext} reloaded!")

client.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(
    name="in development",
    type=hikari.ActivityType.PLAYING
    )
)

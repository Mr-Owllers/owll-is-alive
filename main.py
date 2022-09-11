"""a discord bot made in python"""
import json
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from logpy import Logger
from logpy.log import Level, Format
from logpy.ansi import ForegroundColor, BackgroundColor, Effect

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

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

def main():
    """main function"""
    help_command = commands.DefaultHelpCommand(no_category="Other Commands")

    def get_prefix(_client, message):
        """get prefix function"""
        with open("prefix.json", "r", encoding="utf-8") as file:
            prefixes = json.load(file)

        guild_id = str(message.guild.id)
        if guild_id in prefixes:
            prefix = prefixes[guild_id]
        else:
            prefix = "owl."  # Prefix defaults to this if none is set for the server
        return prefix

    client = commands.Bot(
        command_prefix = get_prefix,
        help_command = help_command,
        intents=intents
    )

    with open("owners.json", "r", encoding="utf-8") as file:
        owners = json.load(file)


    @client.event
    async def on_ready():
        logger.log("owll is alive!", info)
        await client.change_presence(
            status=nextcord.Status.online,
            activity=nextcord.Game("bing chilling | owl.help"))


    @client.command(help="change the prefix", aliases=["pre", "prefix", "prfx"])
    @commands.has_permissions(administrator=True)
    async def setprefix(ctx, *args):
        if len(args) < 1:
            await ctx.send("No prefix specified!")
            return

        prefix = args[0]

        if len(prefix) > 6:
            await ctx.send(
                "Prefix has more characters than the character limit! (6)")
            return

        with open("prefix.json", "r", encoding="utf-8") as file:
            prefixes = json.load(file)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefix.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(prefixes, indent=4))

        await ctx.send(f"Prefix set to {prefix}")
        await ctx.guild.get_member(client.user.id).edit(nick=f"[{prefix}] owll")
        await ctx.send(
            f"Changed nickname to [{prefix}] owll")

    @client.command(hidden=True)
    async def load(ctx, extension):
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} loaded")


    @client.command(hidden=True)
    async def unload(ctx, extension):
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} unloaded")


    @client.command(hidden=True)
    async def reload(ctx, extension):
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        client.reload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} reloaded")


    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")


    @client.command(help="Shows the ping/latency of the bot in miliseconds.",
                    brief="Shows ping")
    async def ping(ctx):
        await ctx.send(f"🏓 Pong!\n{round(client.latency * 1000)}ms")


    @client.command(help="see how many servers the bot is in")
    async def bot_in(ctx):
        await ctx.send(f"I'm in {len(client.guilds)} servers")


    @client.command(hidden=True)
    async def bot_in_o(ctx):
        if ctx.message.author.id not in owners:
            return
        await ctx.send("\n".join(guild.name for guild in client.guilds))

    @client.event
    async def on_command_error(
        ctx, error
    ):
        if isinstance(error, commands.CommandOnCooldown
                    ):  #command is on cooldown.
            msg = f"Still on cooldown, please try again in {error.retry_after}s."
            em13 = nextcord.Embed(
                title="**Error Block**",
                color=nextcord.Color.red())
            em13.add_field(name="__Slowmode Error:__", value=msg)
            await ctx.send(embed=em13
                        )
        if isinstance(
                error, commands.MissingRequiredArgument
        ):  #missing args
            msg2 = "Please enter all the required arguments!"
            em14 = nextcord.Embed(title = f"**{msg2}**")
            em14.add_field(name = "__Expected Arguments:__", value=msg2)
            await ctx.send(embed = em14)
        if isinstance(
                error, commands.MissingPermissions
        ):  #missing perms
            msg3 = "You are missing permissions to use that command!"
            em15 = nextcord.Embed(title = "**Missing permissions**")
            em15.add_field(name = "__Missing Permissions:__", value=msg3)
            await ctx.send(embed = em15)
        if isinstance(
                error, commands.CommandNotFound
        ):  #command not found error.
            msg4 = "No command found!"
            em16 = nextcord.Embed(title = f"**{msg4}**")
            em16.add_field(name = "__Command Not Found:__", value=msg4)
            await ctx.send(embed = em16)
        if isinstance(
                error, commands.CommandInvokeError
        ):  #invalid arg
            msg5 = "Invocation error"
            em17 = nextcord.Embed(title = msg5)
            em17.add_field(name = "__Invocation error__", value = str(error))
            await ctx.send(embed = em17)

    client.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()

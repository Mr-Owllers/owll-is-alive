import json
from datetime import datetime

import hikari
import lightbulb
import psutil

with open("owners.json", "r", encoding="utf-8") as file:
    owners = json.load(file)

@lightbulb.Check
def is_owner(ctx) -> bool:
    return ctx.author.id in owners

plugin = lightbulb.Plugin("misc", include_datastore = True)

plugin.d.counter = datetime.now()

@plugin.command
@lightbulb.command("ping", "Gives the latency of the bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f"🏓 Pong!\n{round(ctx.bot.heartbeat_latency * 1000)}ms")

@plugin.command
@lightbulb.command("stats", "Get statistics info of the bot.", aliases=["status, uptime"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stats(ctx):
    try:
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().uss / 1024 ** 2
        )
    except AttributeError:
        # OS doesn't support retrieval of USS (probably BSD or Solaris)
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().rss / 1024 ** 2
        )
    sysboot = datetime.fromtimestamp(psutil.boot_time()).strftime("%B %d, %Y at %I:%M:%S %p")
    uptime = datetime.now() - plugin.d.counter
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    days, hours = divmod(hours, 24)
    guilds = ctx.bot.cache.get_guilds_view()
    
    if days:
        time = "%s days, %s hours, %s minutes, and %s seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    else:
        time = "%s hours, %s minutes, and %s seconds" % (
            hours, minutes, seconds)
    em = hikari.Embed(title="System Status", color=0x32441C)
    em.add_field(
        name=":gear: Library Version",
        value=f"hikari {hikari.__version__} + Lightbulb {lightbulb.__version__}",
        inline=False,
    )
    em.add_field(
        name="\U0001F4BE BOT Memory usage",
        value=mem_usage,
        inline=False
    )
    em.add_field(
        name="\U0001F553 BOT Uptime",
        value=time,
        inline=False
    )
    em.add_field(
        name="⏲️ Last System Boot Time",
        value=sysboot,
        inline=False
    )
    em.add_field(
        name="🛰️ Servers (Guilds)",
        value=str(len(guilds)),
        inline=False
    )
    await ctx.respond(em)

@plugin.command
@lightbulb.add_checks(is_owner)
@lightbulb.command("bot_in", "see in which servers the bot is in", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def bot_in(ctx):
    guilds = list(ctx.bot.cache.get_available_guilds_view().values())
    await ctx.respond("\n".join(f"{guild.name} : {guild.id}" for guild in guilds))

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)

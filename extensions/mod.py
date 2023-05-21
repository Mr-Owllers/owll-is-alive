import json

import hikari
import lightbulb
from lightbulb.utils import nav, pag

plugin = lightbulb.Plugin("admin", "admin commands")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option("prefix", "set prefix to?")
@lightbulb.command("prefix", "set prefix to?")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def prefix(ctx):
    prfx = ctx.options.prefix
    guild_id = str(ctx.guild_id)
    if len(prfx) > 6:
        await ctx.respond("prefix must be shorter than 6 characters")
        return

    with open("../prefix.json", "r+", encoding="utf-8") as file:
        prefixes = json.load(file)
        
        if prfx == "owl.":
            del prefixes[guild_id]
        else:
            prefixes[guild_id] = prfx

        file.seek(0, 0)
        file.truncate()

        file.write(json.dumps(prefixes, indent=4))

    await ctx.respond(f"Prefix set to {prfx}")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("amount", "amount of messages to purge", int)
@lightbulb.command("purhe", "purge messages", aliases=["clear"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge(ctx):
    num_msgs = ctx.options.messages
    channel = ctx.get_channel()
    messages = list(await channel.fetch_history().limit(num_msgs+ 1))
    await ctx.app.rest.delete_messages(channel, messages)

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("member", "member", hikari.Member, required=True)
@lightbulb.option("reason", "reason", str, required=True)
@lightbulb.command("kick", "kick an annoying member")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def kick(ctx):
    await ctx.options.member.kick(reason=ctx.options.reason)
    await ctx.respond(f"{ctx.options.member.mention} has been kicked")




@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("member", "member", hikari.Member, required=True)
@lightbulb.option("reason", "reason", str, required=True)
@lightbulb.command("ban", "bans the member")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ban(ctx):
    await ctx.options.member.ban(reason=ctx.options.reason)
    await ctx.respond(f"{ctx.options.member.mention} has been banned")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("member", "member", hikari.Member, required=True)
@lightbulb.option("reason", "reason", str, required=True)
@lightbulb.command("unban", "unbans the member")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def unban(ctx):
    await ctx.get_guild().unban(user=ctx.options.member, reason=ctx.options.reason)
    await ctx.respond(f"{ctx.options.member.mention} has been unbanned")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.command("bans", "see the list of banned members in this server")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def bans(ctx):
    banlist = await ctx.bot.rest.fetch_bans(ctx.get_guild())
    lst = pag.EmbedPaginator()

    @lst.embed_factory()
    def build_embed(page_index, page_content):
        emb = hikari.Embed(title="List of Banned Members", description=page_content)
        emb.set_footer(f"{len(banlist)} Members in total.")
        return emb

    if len(banlist) < 1:
        lst.add_line(f"no bans :D")

    else:
        for n, users in enumerate(banlist, start=1):
            lst.add_line(
                f"**{n}. {users.user}**:{users.user.id} ({users.reason or 'No Reason Provided.'})"
            )

    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)

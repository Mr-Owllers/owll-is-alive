import lightbulb
import hikari

ICON = "https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256"
AUTHOR = "Owll"
FOOTER = "<3"

plugin = lightbulb.Plugin("dot", "dootle related commands")

@plugin.command
@lightbulb.option("arg", "what prefix to find", str, default=".")
@lightbulb.command("finddot", "find everyone with a prefix")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def finddot(ctx):
    prefix = ctx.options.arg

    dots = []
    members = ctx.get_guild().get_members().values()
    for member in members:
        nick = member.nickname
        if member.nickname == None:
            nick = member.username

        if nick.startswith(prefix.lower()) or nick.startswith(prefix.upper()):
            dots.append(f"{member.username}#{member.discriminator}")

    if dots:
        amount = len(dots)

        plural = amount > 1

        if not plural:
            message = f"{amount} user with prefix \"{prefix}\" is in this server"
        else:
            message = f"{amount} users with prefix \"{prefix}\" are in this server"

        embed = hikari.Embed(
            title = f"All the \"{prefix}\"s",
            description = "\n".join(dots),
            color = 0x2b6ed9
        )
        embed.set_footer(message)

        await ctx.respond(embed)
    else:
        await ctx.respond(f"No users with prefix \"{prefix}\" found")
        
@plugin.command
@lightbulb.command("whydot", "wtf r dot commands?")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def whydot(ctx):
    embed = hikari.Embed(
        title="why dot???",
        description="its an inside joke from [dootle ville](https://dsc.gg/dootle)",
        color = 0x2b6ed9
    )
    embed.set_author(name=AUTHOR, icon=ICON)
    embed.set_footer(FOOTER)
    await ctx.respond(embed)

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)
"""dottle ville"""
import nextcord
from nextcord.ext import commands

ICON = """
    https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256
"""
AUTHOR = "Owll"
FOOTER = "luv ya!"

class Dot(commands.Cog, description="dootle ville (https://dsc.gg/dottle)"):
    """cog init"""
    def __init__(self, client):
        self.client = client

    @commands.command(
        help = "find ppl with the same prefix",
        name = "finddot",
        aliases = [
          "findprefix",
          "finduserswithprefix"
        ]
    )
    async def find_dot(self, ctx, *args):
        """find ppl with the same prefix"""
        if not args:
            args = ["."]

        async with ctx.typing():
            prefix = " ".join(args)

            dots = []

            for member in ctx.guild.members:
                if not member.nick:
                    member.nick = member.name

                if member.nick.startswith(prefix):
                    dots.append(f"{member.name}#{member.discriminator}")

            if dots:
                amount = len(dots)

                plural = amount > 1

                if not plural:
                    message = f"{amount} user with prefix \"{prefix}\" is in this server"
                else:
                    message = f"{amount} users with prefix \"{prefix}\" are in this server"

                await ctx.send(message)

                await ctx.send(
                embed = nextcord.Embed(
                    title = f"All the \"{prefix}\"s",
                    description = "\n".join(dots),
                    color = ctx.author.color
                )
                )
            else:
                message = f"No users with prefix \"{prefix}\" found"
                await ctx.send(message)

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def undot(self, ctx):
        """remove prefix from nick"""
        for member in ctx.guild.members:
            nick = member.name
            try:
                await member.edit(nick = nick)
            except nextcord.Forbidden as error:
                await ctx.send(error)

            await ctx.send("unprefixed everyone")

    @commands.command(
        help = "prefix everyone in the server",
        aliases = ["prefix_all"]
    )
    @commands.has_permissions(manage_nicknames=True)
    async def dot(self, ctx, *args):
        """prefix everyone in the server"""
        if not args:
            args = ["."]
        prefix = " ".join(args)

        for member in ctx.guild.members:
            nick = f"{prefix} but {member.name}"
            try:
                await member.edit(nick=nick)
            except nextcord.Forbidden as error:
                await ctx.send(error)

        await ctx.send(f"prefixed everyone with {prefix}")

    @commands.command(help="why dot??")
    async def whydot(self, ctx):
        """why dot??"""
        embed = nextcord.Embed(
            title="why dot???",
            description="its an inside joke from [dootle ville](https://dsc.gg/dootle)",
            color = ctx.author.color
        )
        embed.set_author(name = AUTHOR, icon_url = ICON)
        embed.set_footer(text = FOOTER)
        await ctx.send(embed = embed)

def setup(client):
    """cog setup"""
    client.add_cog(Dot(client))

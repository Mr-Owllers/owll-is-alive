"""admin commands"""
import nextcord
from nextcord.ext import commands

class Admin(commands.Cog, description="admin commands"):
    """cog init"""
    def __init__(self, client):
        self.client = client

    @commands.command(help= "delete messages in bulk", aliases=["purge", "c"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount = 5):
        """bulk delete messages"""
        await ctx.channel.purge(limit = amount + 1)
        await ctx.send(f"{amount} messages deleted" , delete_after = 5)

    @commands.command(help= "kick a member", aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        """kick a member"""
        author = ctx.author

        if member == author:
            await ctx.send("you can't kick yourself")
        else:
            try:
                await member.kick(reason=reason)
                await member.send(
                        f"```\nyou were kicked from {ctx.guild.name}\nreason={reason}\n```"
                    )
                await ctx.send(
                    f"```\n{member} was kicked by {ctx.author.name}\nreason={reason}\n```"
                )
            except nextcord.Forbidden:
                await member.kick(reason=reason)
                await ctx.send(
                    f"```\n{member} was kicked by {ctx.author.name}\nreason={reason}\n```"
                )

    @commands.command(help= "ban a member", aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """ban a member"""
        author = ctx.author

        if member == author:
            await ctx.send("you can't ban yourself")
        else:
            try:
                await member.ban(reason=reason)
                await member.send(
                    f"```\nyou were banned from {ctx.guild.name}\nreason={reason}\n```"
                )
                await ctx.send(
                    f"```\n{member} was banned by {ctx.author.name}\nreason={reason}\n```"
                )
            except nextcord.Forbidden:
                await member.ban(reason=reason)
                await ctx.send(
                    f"```\n{member} was banned by {ctx.author.name}\nreason={reason}\n```"
                )

    @commands.command(help = "see how many ppl you banned")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        """see how many ppl you banned"""
        async for entry in ctx.guild.bans():
            pretty_list = [
                f"• {entry.user.id} ({entry.user.name}#{entry.user.discriminator}) - {entry.reason}"
            ]
            await ctx.send("**Ban list:** ```\n{}```".format("\n".join(pretty_list)))

    @commands.command(help="unban a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """unban a member"""
        banned = await ctx.guild.bans()
        member_name, member_discrim = member.split("#")

        for ban_entry in banned:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discrim):
            await ctx.guild.unban(user)
            await ctx.send(
                f"```\n{user.name}#{user.discriminator} was unbanned by {ctx.author.name}\n```"
            )
            return

def setup(client):
    """cog setup"""
    client.add_cog(Admin(client))

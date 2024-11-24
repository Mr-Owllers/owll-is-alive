import json
from sys import flags
import discord
from discord.ext import commands
from dpy_paginator import paginate

class Moderation(commands.Cog, description="mod stuff"):
    def __init__(self, bot):
        self.bot = bot
        
    class DefaultFlags(commands.FlagConverter):
        member: discord.Member = commands.flag(description="the member to act on")
        reason: str = commands.flag(default=None, description="the reason for the action")
        
    class UnbanFlags(commands.FlagConverter):
        member: str = commands.flag(description="the member to unban")
        reason: str = commands.flag(default=None, description="the reason for the action")
        
    class NickFlags(commands.FlagConverter):
        member: discord.Member = commands.flag(description="the member to act on")
        nickname: str = commands.flag(description="the new nickname")

    @commands.hybrid_command(help="kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, flags: DefaultFlags):
        await flags.member.kick(reason=flags.reason)
        await ctx.send(f"{flags.member.mention} has been kicked.")

    @commands.hybrid_command(help="ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, flags: DefaultFlags):
        await flags.member.ban(reason=flags.reason)
        await ctx.send(f"{flags.member.mention} has been banned.")

    @commands.hybrid_command(help="unban a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, flags: UnbanFlags):
        banned_users = await ctx.guild.bans()
        if flags.member.isdigit():
            user = discord.Object(id=int(flags.member))
        elif flags.member.startswith("<@") and flags.member.endswith(">"):
            user = discord.Object(id=int(flags.member[2:-1]))
        else:
            user = discord.utils.get(banned_users, name=flags.member)
            if user is None:
                raise commands.BadArgument

        if user not in banned_users:
            await ctx.send("User is not banned.")
            return

        await ctx.guild.unban(user, reason=flags.reason)
        await ctx.send(f"{user.name} has been unbanned.")

    @commands.hybrid_command(help="check bans")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        banlist = [entry async for entry in ctx.guild.bans()]
        embeds = []
        if len(banlist) < 1:
            embed = discord.Embed(
                title="Bans",
                description=f"in {ctx.guild.name}",
                color=ctx.author.color
            )
            embed.add_field(
                name="No bans found",
                value=":D",
                inline=False
            )
            embeds.append(embed)
        else:
            for i in range(0, len(banlist), 20):
                bans = banlist[i:i+20]
                embed = discord.Embed(
                    title=f"Bans",
                    description=f"in {ctx.guild.name}",
                    color=ctx.author.color
                )
                for n, users in enumerate(bans):
                    embed.add_field(
                        name=f"Banned #{n+1}",
                        value=f"{users.user} ({users.user.id}): {users.reason}",
                        inline=False
                    )

                embeds.append(embed)

        output = paginate(embeds=embeds)
        await ctx.send(embed=output.embed, view=output.view)

    @commands.hybrid_command(help="purge messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 5):
        if limit < 1 or limit > 100:
            return await ctx.send("Invalid limit. Must be between 1 and 100")
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"{limit} messages deleted", delete_after=5)

    @commands.hybrid_command(help="change the prefix")
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix: str = "owl."):
        with open("data/prefix.json", "r") as f:
            prefix = json.load(f)

        if prefix.get(str(ctx.guild.id)) == new_prefix:
            await ctx.send("Prefix is already the same")
        elif new_prefix == "owl.":
            if str(ctx.guild.id) in prefix:
                prefix.pop(str(ctx.guild.id))
                with open("data/prefix.json", "w") as f:
                    json.dump(prefix, f, indent=4)
            await ctx.send("Prefix removed")
        else:
            prefix[str(ctx.guild.id)] = new_prefix
            with open("data/prefix.json", "w") as f:
                json.dump(prefix, f, indent=4)

        # get ctx.guild.me.display_name but remove everything in []
        name = ctx.guild.me.display_name if "[" not in ctx.guild.me.display_name else ctx.guild.me.display_name.split("]")[1].strip()

        await ctx.send(f"Prefix changed to {new_prefix}")
        await ctx.guild.me.edit(nick=f"[{new_prefix}] {name}")

    @commands.hybrid_command(help="set nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, flags: NickFlags):
        await flags.member.edit(nick=flags.nickname)
        await ctx.send(f"{flags.member.mention}'s nickname has been changed to {flags.nickname}")


async def setup(bot):
    await bot.add_cog(Moderation(bot))

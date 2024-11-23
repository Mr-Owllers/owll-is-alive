import json
import discord
from discord.ext import commands
from dpy_paginator import paginate

class Moderation(commands.Cog, description="mod stuff"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked.")

    @commands.hybrid_command(help="ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned.")

    @commands.hybrid_command(help="unban a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        if member.isdigit():
            user = discord.Object(id=int(member))
        elif member.startswith("<@") and member.endswith(">"):
            user = discord.Object(id=int(member[2:-1]))
        else:
            user = discord.utils.get(banned_users, user__name=member)
            if user is None:
                raise commands.BadArgument

        if user not in banned_users:
            await ctx.send("User is not banned.")
            return

        await ctx.guild.unban(user)
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
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"{limit} messages deleted", delete_after=5)

    @commands.hybrid_command(help="change the prefix")
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix):
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
    async def nick(self, ctx, member: discord.Member, *, nickname):
        await member.edit(nick=nickname)
        await ctx.send(f"{member.mention}'s nickname has been changed to {nickname}")


async def setup(bot):
    await bot.add_cog(Moderation(bot))

import discord
from discord.ext import commands
from dpy_paginator import paginate

ICON = "https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256"
AUTHOR = "Owll"
FOOTER = "<3"

class Dot(commands.Cog, description="dootle joke"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="find ppl with the same prefix")
    async def finddot(self, ctx, *, args):
        if not args:
            args = ["."]

        async with ctx.typing():
            prefix = " ".join(args)

            dots = []

            for member in ctx.guild.members:
                if member.display_name.startswith(prefix) or member.name.startswith(prefix):
                    dots.append(f"{member.display_name} ({member.name}#{member.discriminator} : {member.id})")

            if dots:
                ems = []
                for i in range(0, len(dots), 25):
                    doties = sorted(dots[i:i+25])
                    em = discord.Embed(
                        title=f"Users with prefix {prefix}",
                        color=discord.Color.green(),
                    )
                    for n, dot in enumerate(doties):
                        em.add_field(
                            name=f"{n+1}.",
                            value=dot,
                            inline=False
                        )

                    em.set_author(name=AUTHOR, icon_url=ICON)
                    em.set_footer(text=FOOTER)
                    ems.append(em)

                output = paginate(embeds=ems)
                await ctx.send(embed=output.embed, view=output.view)
            else:
                message = f'No users with prefix "{prefix}" found'
                await ctx.send(message)

    @commands.hybrid_command(help="why dot??")
    async def whydot(self, ctx):
        """why dot??"""
        embed = discord.Embed(
            title="why dot???",
            description="its an inside joke from dootle ville (a friend's server)",
            color=ctx.author.color,
        )
        embed.set_author(name=AUTHOR, icon_url=ICON)
        embed.set_footer(text=FOOTER)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dot(bot))

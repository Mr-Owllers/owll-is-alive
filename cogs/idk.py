"""random commands idk"""
import random

import aiohttp
import nextcord
from nextcord.ext import commands

ICON = """
    https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256
"""
AUTHOR = "Owll"
FOOTER = "luv ya!"
hug = ["https://c.tenor.com/bFZKN-tlQP4AAAAC/love-you-my-best-friend.gif",
    "https://c.tenor.com/KlkE8vt8gOIAAAAM/love-is-the-answer-to-everything-hug.gif",
    "https://c.tenor.com/OkpKo5iPu-8AAAAM/huge-hug.gif",
    "https://c.tenor.com/BW8ZMOHHrgMAAAAM/friends-joey-tribbiani.gif",
    "https://c.tenor.com/ut3cq1GezaoAAAAM/hug-hugs.gif",
    "https://media1.tenor.com/images/8ac5ada8524d767b77d3d54239773e48/tenor.gif?itemid=16334628",
    "https://c.tenor.com/0gz0aKX9vcQAAAAC/owl-hug-sweet.gif"
]


class General(commands.Cog, name="Random", description="idk"):
    """cog init"""
    def __init__(self, client):
        self.client = client

    @commands.command(help="Invite me!", aliases=["inv", "i"])
    async def invite(self, ctx):
        """invite me"""
        embed = nextcord.Embed(
            title="Invite me!",
            description="Invite me by pressing [here](https://dsc/owll)",
            color=ctx.author.color
        )
        embed.set_author(name = AUTHOR, icon_url = ICON)
        embed.set_footer(text = FOOTER)

        await ctx.message.reply(embed=embed)

    @commands.command(
        help="get a link to the support server",
        aliases=["xtrahelp", "extrahelp", "helpme"]
    )
    async def support(self, ctx):
        """get a link to the support server"""
        embed = nextcord.Embed(
            title="Support server",
            description="You may join our [support server](https://dsc.gg/owlly) :D",
            color=ctx.author.color
        )
        embed.set_author(name = AUTHOR, icon_url = ICON)
        embed.set_footer(text = FOOTER)

        await ctx.message.reply(embed=embed)

    @commands.command(help="hug someone!")
    async def hug(self, ctx, members: commands.Greedy[nextcord.Member]):
        """hug someone"""
        async with aiohttp.ClientSession() as c_s:
            async with c_s.get("https://some-random-api.ml/animu/hug") as read:
                j_s = await read.json()

                if not members:
                    return await ctx.send("Please specify someone to hug.")

                if ctx.author in members:
                    return await ctx.send("you hug yourself... somehow")

                embed = nextcord.Embed(
                    color=0xff0000,
                    description=f"**{ctx.author.name}** hugs "+ "**" +
                    '**, **'.join(x.display_name for x in members) + "**! Awwww!")

                manual = hug
                manual.append(j_s['link'])
                image = random.choice(manual)

                embed.set_image(url=image)
                await ctx.send(embed=embed)

def setup(client):
    """cog setup"""
    client.add_cog(General(client))

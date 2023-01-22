import random

import aiohttp
import hikari
import lightbulb

ICON = "https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256"
AUTHOR = "Owll"
FOOTER = "<3"
huglist = ["https://c.tenor.com/bFZKN-tlQP4AAAAC/love-you-my-best-friend.gif",
    "https://c.tenor.com/KlkE8vt8gOIAAAAM/love-is-the-answer-to-everything-hug.gif",
    "https://c.tenor.com/OkpKo5iPu-8AAAAM/huge-hug.gif",
    "https://c.tenor.com/BW8ZMOHHrgMAAAAM/friends-joey-tribbiani.gif",
    "https://media1.tenor.com/images/8ac5ada8524d767b77d3d54239773e48/tenor.gif?itemid=16334628",
    "https://c.tenor.com/0gz0aKX9vcQAAAAC/owl-hug-sweet.gif"
]

plugin = lightbulb.Plugin("random", "some random commands")

@plugin.command
@lightbulb.command("invite", "invite me to ur server!", aliases=["inv", "i"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def invite(ctx):
    embed = hikari.Embed(
        title="Invite me!",
        description="Invite me by pressing [here](https://dsc/owll)",
        color=0x2b6ed9
    )
    embed.set_author(name=AUTHOR, icon=ICON)
    embed.set_footer(FOOTER)

    await ctx.respond(embed, reply=True)

@plugin.command
@lightbulb.command("support", "join server for extra help")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def support(ctx):
    embed = hikari.Embed(
        title="Support server",
        description="You may join our [support server](https://dsc.gg/owlly) :D",
        color=0x2b6ed9
    )
    embed.set_author(name=AUTHOR, icon=ICON)
    embed.set_footer(FOOTER)

    await ctx.respond(embed, reply=True)

@plugin.command
@lightbulb.option("target", "The member you wish to hug.", hikari.Member)
@lightbulb.command("hug", "hug someone in the server!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def hug(ctx):
    target_ = ctx.options.target
    # Convert the option into a Member object if lightbulb couldn't resolve it automatically
    target = (
        target_
        if isinstance(target_, hikari.Member)
        else ctx.get_guild().get_member(target_)
    )
    if not target:
        await ctx.respond("That user is not in the server.")
        return

    if ctx.author.id == target.id:
        await ctx.respond("PFFFF! did u just try to hug urself? bro get a LIFE!")
        return

    a = random.randint(1, 100)
    b = [2, 87, 34, 98, 9, 32, 45, 15, 37, 78, 35, 83, 95, 14, 82, 73, 17, 92, 8, 20]

    if a in b: #1/5 chance of getting unlucky
        await ctx.respond(f"{target.username} ran away before u could hug them. LOL! u unlucky af!")
        return

    async with aiohttp.ClientSession() as c_s:
            async with c_s.get("https://some-random-api.ml/animu/hug") as res:
                if res.ok:
                    res = await res.json()
                    huglist.append(res["link"])
                    link = random.choice(huglist)
                    deco = ["cute!", "awwww!", "^w^"]
                    decor = random.choice(deco)
                    embed = hikari.Embed(description=f"**{ctx.member.username}** hugs **{target.username}**... {decor}", colour=0x3B9DFF)
                    embed.set_image(link)

    await ctx.respond(embed)

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)
import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
import typing

class Actions(commands.Cog, description="interact using gifs!"):
    def __init__(self, bot):
        self.bot = bot

    class InteractFlags(commands.FlagConverter):
        action: typing.Literal[
            "hug", "pat", "slap", "kiss", "poke", "feed", "bite", 
            "cuddle", "stare", "tickle", "wave", "highfive", "handhold", 
            "wink", "handshake", "baka", "kick", "punch", "peck", "shoot", "yeet"
        ] = commands.flag(description="the action to perform")
        member: discord.Member = commands.flag(description="the member to interact with")

    class ReactFlags(commands.FlagConverter):
        action: typing.Literal[
            "blush", "bored", "cry", "dance", "facepalm", "happy", "laugh",
            "lurk", "nod", "nom", "nope", "pout", "shrug", "smile", "smug",
            "think", "thumbsup", "yawn"
        ] = commands.flag(description="the action to perform")

    @commands.hybrid_command(help="interact with someone!")
    async def interact(self, ctx, flags: InteractFlags):
        actions = [
            "hug", "pat", "slap", "kiss", "poke", "feed", "bite", 
            "cuddle", "stare", "tickle", "wave", "highfive", "handhold", 
            "wink", "handshake", "baka", "kick", "punch", "peck", "shoot", "yeet"
        ]
        if ctx.author == flags.member:
            if flags.action in ["hug", "pat", "cuddle", "wave", "handhold", "highfive"]:
                return await ctx.send("lol loser!")
            elif flags.action in ["kiss", "peck", "wink", "handshake", "stare", "kick"]:
                return await ctx.send("uhh how would you even do that to yourself?")
            elif flags.action in ["baka", "poke", "tickle"]:
                return await ctx.send("...you're weird")
            elif flags.action in ["slap", "punch", "shoot", "yeet"]:
                return await ctx.send("please dont do that! :(") 
            elif flags.action == "feed":
                return await ctx.send("you ate some food! yay!\n(for a gif, do `<prefix>react nom`)")

        if flags.action not in actions:
            return await ctx.send(f"Invalid action! Choose from: ```{', '.join(actions)}```")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekos.best/api/v2/{flags.action}") as response:
                data = await response.json()
                data = data["results"][0]
                embed = discord.Embed(
                    color=ctx.author.color,
                    timestamp=datetime.now()
                )
                if flags.action in ["kiss", "punch"]:
                    embed.title = f"{ctx.author.name} {flags.action}es {flags.member.name}"
                elif flags.action in ["stare", "wave", "wink"]:
                    embed.title = f"{ctx.author.name} {flags.action}s at {flags.member.name}"
                elif flags.action == "baka":
                    embed.title = f"{ctx.author.name} calls {flags.member.name} a baka"
                elif flags.action == "handhold":
                    embed.title = f"{ctx.author.name} holds {flags.member.name}'s hand"
                else:
                    embed.title = f"{ctx.author.name} {flags.action}s {flags.member.name}"
                embed.set_footer(text=f"gif from {data["anime_name"]}")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    # reactions
    @commands.hybrid_command(help="do a reaction!", aliases=["act"])
    # async def react(self, ctx, action):
    # show all the actions available when using slash commands
    async def react(self, ctx, flags: ReactFlags):
        actions = [
            "blush", "bored", "cry", "dance", "facepalm", "happy", "laugh",
            "lurk", "nod", "nom", "nope", "pout", "shrug", "smile", "smug",
            "think", "thumbsup", "yawn"
        ]

        if flags.action not in actions:
            return await ctx.send(f"Invalid action! Choose from: ```{', '.join(actions)}```")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekos.best/api/v2/{flags.action}") as response:
                data = await response.json()
                data = data["results"][0]
                embed = discord.Embed(
                    title=f"{ctx.author.name} {flags.action}s",
                    color=ctx.author.color,
                    timestamp=datetime.now(),
                )
                embed.set_footer(text=f"gif from {data["anime_name"]}")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Actions(bot))

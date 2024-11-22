import discord
from discord.ext import commands
import aiohttp
import datetime

class Actions(commands.Cog, description="interact using gifs!"):
    def __init__(self, bot):
        self.bot = bot

    # interactive
    @commands.hybrid_command(help="hug someone")
    async def hug(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/hug") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} hugs {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(help="pat someone")
    async def pat(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/pat") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} pats {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(help="slap someone")
    async def slap(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/slap") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} slaps {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(help="kiss someone")
    async def kiss(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/kiss") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} kisses {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="poke someone")
    async def poke(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/poke") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} pokes {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="feed someone")   
    async def feed(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/feed") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} feeds {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="nom someone")
    async def nom(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/nom") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} noms {member.name}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                                
    # reactions
    @commands.hybrid_command(help="blush")
    async def blush(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/blush") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} blushes",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="cry")
    async def cry(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/cry") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} cries",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="laugh")
    async def laugh(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/laugh") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} laughs",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="pout")
    async def pout(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/pout") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} pouts",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="smile")
    async def smile(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/smile") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} smiles",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="smug")
    async def smug(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/smug") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} smugs",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="stare")
    async def stare(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/stare") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} stares",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
    @commands.hybrid_command(help="think")
    async def think(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/think") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} thinks",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
             
    @commands.hybrid_command(help="wink")
    async def wink(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/wink") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} winks",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
               
    @commands.hybrid_command(help="facepalm")
    async def facepalm(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/face-palm") as response:
                data = await response.json()
                embed = discord.Embed(
                    title=f"{ctx.author.name} facepalms",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
                
async def setup(bot):
    await bot.add_cog(Actions(bot))

"""the fun cog"""
import random
import nextcord
from nextcord.ext import commands

class Fun(commands.Cog, description="just some fun commands"):
    """cog init"""
    def __init__(self, client):
        self.client=client

    @commands.command(
            help="funny command"
    )
    async def yeet(self, ctx):
        """yeet"""
        await ctx.send("(╯°□°）╯︵ ┻━┻ YAAAA YEEEEEEEET!!!!")

    @commands.command(help="funny command")
    async def unyeet(self, ctx):
        """unyeet"""
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.command(
            name = "8ball",
            help = "ask me anything"
    )
    async def _8ball(self, ctx, *, question):
        """8ball"""
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.",
                "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "It is certain.", "It is decidedly so.",
                "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.",
                "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes - definitely.", "You may rely on it."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(
            help="filps a coin... duh"
    )
    async def coinflip(self, ctx):
        """coinflip"""
        flip = ['heads', 'tails']
        await ctx.send(f'{random.choice(flip)}')

    @commands.command(
            help="in choice use 👊, ✌️, ✋, rock, paper or scissors"
    )
    async def rps(self, ctx, choice):
        """rock paper scissors"""
        p_c=['👊', '✌️', '✋', 'rock', 'paper', 'scissors']
        choices=['👊', '✌️', '✋']
        if choice not in p_c:
            await ctx.send(
                "error: please put :punch:, :raised_hand:, :v:, rock, paper or scissors"
                )
        else:
            await ctx.send(random.choice(choices))

    @commands.command(
            help="in choice use 👊, 🐶, ✋, punch, pet assist, slap"
    )
    async def fight(self, ctx, choice):
        """fight the bot"""
        p_f=['👊', '🐶', '✋', 'punch', 'pet', 'slap']
        fight=['I 👊 (punch)', 'My 🐶 (pet) bites', 'I ✋ (slap)']
        dam=['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65',
            '70', '75', '80', '85', '90', '95', '100']
        if choice not in p_f:
            await ctx.send(
                "error: please put :punch:, :raised_hand:, :dog:, punch, slap or pet"
                )
        else:
            await ctx.send(
                f"{random.choice(fight)} you\nI deal {random.choice(dam)}% damage\n" +
                f"You deal {random.choice(dam)}% damage" #added the + to make pylint happy
                )

    @commands.command(help="make the bot say something", aliases=["say", "print"])
    async def echo(self, ctx, *, saysen):
        """echo in a channel"""
        embed = nextcord.Embed(title="say command", description=f"{saysen}", color=0xe397f2)
        embed.set_footer(text=f"by {ctx.author.name}")
        await ctx.send(embed=embed)

def setup(client):
    """cog setup"""
    client.add_cog(Fun(client))

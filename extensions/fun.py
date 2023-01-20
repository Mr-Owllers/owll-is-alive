import random

import hikari
import lightbulb

plugin = lightbulb.Plugin("fun", "random fun commands")

@plugin.command
@lightbulb.command("yeet", "YEET!!!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def yeet(ctx):
    await ctx.respond("(╯°□°）╯︵ ┻━┻ YEEEEEEEET!!!!")

@plugin.command
@lightbulb.command("unyeet", "hmmm...")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def unyeet(ctx):
    await ctx.respond("┬─┬ ノ( ゜-゜ノ)")

@plugin.command
@lightbulb.option("question", "ask the question", type=str, required=True)
@lightbulb.command("11ball", "the great magic 11ball")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def _11ball(ctx):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.",
                "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "It is certain.", "It is decidedly so.",
                "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.",
                "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes - definitely.", "You may rely on it."]
    await ctx.respond(f'Question: {ctx.options.question}\nAnswer: {random.choice(responses)}')

@plugin.command
@lightbulb.option("item", "choose what u pick", type=str, required=True)
@lightbulb.command("rps", "rock, paper, scissors")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def rps(ctx):
    player = ctx.options.item
    choices = random.choice(["👊", "✋", "✌️"])
    if player == "r":
        if choices == "👊":
            await ctx.respond("u chose 👊\ni chose 👊\ndraw")
        elif choices == "✋":
            await ctx.respond("u chose 👊\ni chose ✋\nyou lose")
        else:
            await ctx.respond("u chose 👊\ni chose ✌️\nyou win")
    elif player == "p":
        if choices == "👊":
            await ctx.respond("u chose ✋\ni chose 👊\nyou win")
        elif choices == "✋":
           await ctx.respond("u chose ✋\ni chose ✋\ndraw")
        else:
            await ctx.respond("u chose ✋\ni chose ✌️\nyou lose")
    elif player == "s":
        if choices == "👊":
            await ctx.respond("u chose ✌️\ni chose 👊\nyou lose")
        elif choices == "✋":
           await ctx.respond("u chose ✌️\ni chose ✋\nyou win")
        else:
            await ctx.respond("u chose ✌️\ni chose ✌️\ndraw")
    else:
        await ctx.respond("choose r, p or s!")

@plugin.command
@lightbulb.option("text", "what to say", type=str, required=True)
@lightbulb.command("echo", "echo... echo... echo", aliases=["say"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo(ctx):
    await ctx.respond(ctx.options.text)

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)

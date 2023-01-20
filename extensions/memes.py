import os
import random

import hikari
import praw
from dotenv import load_dotenv
import lightbulb

load_dotenv()

SECRET = os.environ['SECRET']
ID = os.environ['ID']

reddit = praw.Reddit(
    client_id= ID, client_secret= SECRET, user_agent= "owllAPI", check_for_async=False
)

plugin = lightbulb.Plugin("memes", "bing chillin")

@plugin.command
@lightbulb.option("subred", "where to find sauce", type=str, default="memes")
@lightbulb.command("reddit", "bananas", aliases=["memes"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def memes(ctx):
    red = str(ctx.options.subred)
    sub = reddit.subreddit(red)
    all_subs = []

    hot = sub.hot(limit = 50)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    all_subs.remove(random_sub)

    name = random_sub.title
    url = random_sub.url
    link = random_sub.permalink
    ups = random_sub.score
    comments = random_sub.num_comments
    author = random_sub.author.name

    embed = hikari.Embed(
        title=name, url=f"https://reddit.com/{link}", color=0x2869c9
    )
    embed.set_image(url)
    embed.set_footer(
        text=f"posted in r/{red} | posted by {author} | {ups} upvotes |" +
        f"{comments} comments | requested by {ctx.author.username}"
    )

    if submission.over_18:
        await ctx.respond("this post is nsfw :(")
    else:
        await ctx.respond(embed = embed)

@plugin.command
@lightbulb.add_checks(lightbulb.nsfw_channel_only)
@lightbulb.option("subred", "where to find memes", type=str, default="nsfw")
@lightbulb.command("reddit-nsfw", "black bananas", aliases=["nsfw"], nsfw=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nsfw(ctx):
    red = str(ctx.options.subred)
    sub = reddit.subreddit(red)
    all_subs = []

    hot = sub.hot(limit = 50)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    all_subs.remove(random_sub)

    name = random_sub.title
    url = random_sub.url
    link = random_sub.permalink
    ups = random_sub.score
    comments = random_sub.num_comments
    author = random_sub.author.name

    embed = hikari.Embed(
        title=name, url=f"https://reddit.com/{link}", color=0x2869c9
    )
    embed.set_image(url)
    embed.set_footer(
        text=f"posted in r/{red} | posted by {author} | {ups} upvotes |" +
        f"{comments} comments | requested by {ctx.author.username}"
    )

    await ctx.respond(embed = embed)

def load(client):
    client.add_plugin(plugin)

def unload(client):
    client.remove_plugin(plugin)
import os
import random

import discord
from discord.ext import commands
import praw
from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ["SECRET"]
ID = os.environ["ID"]

reddit = praw.Reddit(
    client_id=ID, client_secret=SECRET, user_agent="owllAPI", check_for_async=False
)

class Memes(commands.Cog, description="MEMES!"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="get a random meme from reddit")
    async def reddit(self, ctx, *, subred="memes"):
        async with ctx.typing():
            try:
                sub = reddit.subreddit(subred)
                all_subs = []

                hot = sub.hot(limit=50)

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

                embed = discord.Embed(
                    title=name, url=f"https://reddit.com{link}", color=ctx.author.color
                )
                embed.set_image(url=url)
                embed.set_footer(
                    text=f"posted in r/{subred} | posted by {author} | {ups} upvotes |"
                    + f"{comments} comments | requested by {ctx.author.name}"
                )

                if submission.over_18:
                    if not ctx.channel.is_nsfw():
                        raise commands.NSFWChannelRequired(ctx.channel)
                    else:
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"oops, ig that subreddit has some problems? likely banned!\n```diff\n-ERROR: {e}```")
    
    @commands.hybrid_command(help="get a random nsfw post from reddit")
    async def nsfw(self, ctx, subred="hentai"):
        async with ctx.typing():
            try:
                sub = reddit.subreddit(subred)
                all_subs = []

                hot = sub.hot(limit=50)

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

                embed = discord.Embed(
                    title=name, url=f"https://reddit.com{link}", color=ctx.author.color
                )
                embed.set_image(url=url)
                embed.set_footer(
                    text=f"posted in r/{subred} | posted by {author} | {ups} upvotes |"
                    + f"{comments} comments | requested by {ctx.author.name}"
                )
                if not ctx.channel.is_nsfw():
                    raise commands.NSFWChannelRequired(ctx.channel)
                else:
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"oops, ig that subreddit has some problems? likely banned!\n```diff\n-ERROR: {e}```")

async def setup(bot):
    await bot.add_cog(Memes(bot))
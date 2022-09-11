"""meme commands"""
import os
import random

import nextcord
import praw
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()

SECRET = os.environ['SECRET']
ID = os.environ['ID']

reddit = praw.Reddit(
    client_id= ID, client_secret= SECRET, user_agent= "owllAPI", check_for_async=False
)


class Memes(commands.Cog, description="MEMES!"):
    """cog init"""
    def __init__(self, client):
        self.client=client

    @commands.command(help="search memes from reddit")
    async def reddit(self, ctx, *, subred="memes"):
        """search memes from reddit"""
        async with ctx.typing():
            sub = reddit.subreddit(subred)
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

            embed = nextcord.Embed(
                title=name,url=f"https://reddit.com{link}", color=ctx.author.color
            )
            embed.set_image(url = url)
            embed.set_footer(
                text=f"posted in r/{subred} | posted by {author} | {ups} upvotes |" +
                f"{comments} comments | requested by {ctx.author.name}"
            ) #added + to make pylint happy

            if submission.over_18:
                if not ctx.channel.is_nsfw():
                    await ctx.send("the post is nsfw")
                else:
                    await ctx.send(embed = embed)
            else:
                await ctx.send(embed = embed)

  # @commands.command(help = "sends a post from a specific sub every random hours")
  # @commands.has_permissions(administrator=True)
  # async def setup_reddit(self, ctx, sub="memes", chan="reddit"):
  #   await ctx.send("setup completed!")
  #   server = ctx.guild.id
  #   db[server] = [sub, chan]


def setup(client):
    """cog setup"""
    client.add_cog(Memes(client))

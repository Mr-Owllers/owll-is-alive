from operator import index
import discord
from discord.ext import commands
from dpy_paginator import paginate
import json
from datetime import datetime
import typing

class Toidua(commands.Cog, description="a TODO list like Idea-manager™️"):
    def __init__(self, bot):
        self.bot = bot

    # use flagconverter to add a description for the parameters
    class AddFlags(commands.FlagConverter):
        idea: str = commands.flag(description="the idea")
        note: str = commands.flag(default=None, description="a note for the idea")

    @commands.hybrid_command(help="add an idea to the list")
    # add a description for the parameters
    async def add(self, ctx, flags: AddFlags):
        author_id = str(ctx.author.id)
        with open("data/toidua.json", "r") as f:
            toidua = json.load(f)

        if author_id not in toidua:
            toidua[author_id] = {"ideas": []}

        date = datetime.now().timestamp()
        date = int(date)

        toidua[author_id]["ideas"].append(
            {
                "idea": flags.idea,
                "note": flags.note,
                "status": "OPEN",
                "date": f"<t:{date}:f>",
            }
        )

        with open("data/toidua.json", "w") as f:
            json.dump(toidua, f, indent=4)

        await ctx.send(f"Added idea: {flags.idea}")

    @commands.hybrid_command(help="list your ideas", name="list", aliases=["ideas", "ls", "view"])
    async def _list(self, ctx):
        author_id = str(ctx.author.id)
        with open("data/toidua.json", "r") as f:
            toidua = json.load(f)

        if author_id not in toidua:
            return await ctx.send("You're name isn't registered in the database\nAdd an idea to register")
        elif len(toidua[author_id]["ideas"]) < 1:
            return await ctx.send("You don't have any ideas!")
        else:
            ideas = toidua[author_id]["ideas"]
            pages = []
            for idea in ideas:
                status = idea["status"]
                date = idea["date"]
                note = idea["note"]
                pages.append(f"**{idea['idea'].capitalize()}**\n+ Note: {note}\n+ Status: **{status}**\n+ Date: {date}")

            embeds = []
            for i in range(0, len(pages), 5):
                page = pages[i:i+5]
                embed = discord.Embed(
                    title="Your Ideas",
                    color=ctx.author.color
                )
                embed.set_footer(text="<3")
                for n, idea in enumerate(page):
                    embed.add_field(name=f"Idea {n}:", value=idea, inline=False)

                embeds.append(embed)

            output = paginate(embeds=embeds)
            await ctx.send(embed=output.embed, view=output.view)

    @commands.hybrid_command(help="remove an idea")
    @discord.app_commands.describe(index="the index of the idea")
    async def remove(self, ctx, index: int):
        author_id = str(ctx.author.id)
        with open("data/toidua.json", "r") as f:
            toidua = json.load(f)

        if author_id not in toidua:
            return await ctx.send("You're name isn't registered in the database\nAdd an idea to register")
        elif len(toidua[author_id]["ideas"]) < 1:
            return await ctx.send("You don't have any ideas!")
        else:
            ideas = toidua[author_id]["ideas"]
            if index >= len(ideas):
                return await ctx.send("Invalid index")

            idea = ideas.pop(index)
            with open("data/toidua.json", "w") as f:
                json.dump(toidua, f, indent=4)

        await ctx.send(f"Removed idea: {idea['idea']}")

    @commands.hybrid_command(help="change the status of an idea")
    @discord.app_commands.describe(index="the index of the idea", status="0=OPEN, 1=IN PROGRESS, 2=DONE")
    async def status(self, ctx, index: int, status: typing.Literal[0, 1, 2]):
        author_id = str(ctx.author.id)
        with open("data/toidua.json", "r") as f:
            toidua = json.load(f)

        if author_id not in toidua:
            return await ctx.send("You're name isn't registered in the database\nAdd an idea to register")
        elif len(toidua[author_id]["ideas"]) < 1:
            return await ctx.send("You don't have any ideas!")
        else:
            ideas = toidua[author_id]["ideas"]
            if index >= len(ideas):
                return await ctx.send("Invalid index")

            if status not in [0, 1, 2]:
                return await ctx.send("Invalid status\nCodes:\n0=**OPEN**\n1=**IN PROGRESS**\n2=**DONE**")

            if ideas[index]["status"] == status:
                return await ctx.send("Status is already the same")

            if status == 0:
                status = "OPEN"
            elif status == 1:
                status = "IN PROGRESS"
            elif status == 2:
                status = "DONE"

            with open("data/toidua.json", "w") as f:
                ideas[index]["status"] = status
                json.dump(toidua, f, indent=4)

            await ctx.send(f"Changed status of idea {index} to **{status}**")

async def setup(bot):
    await bot.add_cog(Toidua(bot))        

# import logging
# import re
# import random
# from typing import Optional
# import os
# from dotenv import load_dotenv

import hikari
import lightbulb
# import spotipy
# from lightbulb.utils import nav, pag
# from spotipy.oauth2 import SpotifyClientCredentials

# import lavasnek_rs

# load_dotenv()

# TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
# SPOTCLIENT_ID = os.getenv("SPOTID")
# SPOTCLIENT_SECRET = os.getenv("SPOTSECRET")
# LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")

plugin = lightbulb.Plugin("music", "u like jazz?")

@plugin.command
@lightbulb.command("music", "doot... do dodo doodoo doot...~")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def music(ctx):
    await ctx.respond("currently in development")

def load(client):
    client.add_plugin(plugin)


def unload(client):
    client.remove_plugin(plugin)
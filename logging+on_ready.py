import os
import json
import logging
import requests
import asyncio
import datetime
import sys

user_log = logging.getLogger("user_log")
bot_log = logging.getLogger("bot_log")

fh_user = logging.FileHandler("user.log", mode="a+")
fh_user.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh_user.setFormatter(formatter)
user_log.addHandler(fh_user)
user_log.setLevel(logging.INFO)

fh_bot = logging.FileHandler("bot.log", mode="a+")
fh_bot.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh_bot.setFormatter(formatter)
bot_log.addHandler(fh_bot)
bot_log.setLevel(logging.INFO)

from keep_alive import keep_alive
import discord
import discord.ext
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ui import Button, View

intents= discord.Intents().all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("Bot ist online!")
    bot_log.info("Bot wurde gestartet")
    synced = await tree.sync()
    print('Commands synced : ' + str(len(synced)))
    await tree.sync(guild=discord.Object(id=760108422594166814))
    client.add_view(Ticket())

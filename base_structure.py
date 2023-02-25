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

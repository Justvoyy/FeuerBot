import os
import json
import logging

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

import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
my_secret = os.environ['API-Key']

from keep_alive import keep_alive
import discord
import discord.ext
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions

intents= discord.Intents().all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

if os.path.exists("last_activity.txt"):
   with open("last_activity.txt", "r") as f:
     last_activity = f.read()
else :
  last_activity = "Feuerball07"
@client.event
async def on_ready():
    print("Bot ist online!")
    bot_log.info("Bot wurde gestartet")
    synced = await tree.sync()
    print('Commands synchronisiert : ' + str(len(synced)))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=last_activity))
    await tree.sync(guild=discord.Object(id=760108422594166814))
    if __name__ == "__main__":
      check_twitch_online_streamers.start()
                               
@client.event
async def on_activity_change(after):
    with open("last_activity.txt", "w") as f:
        f.write(after.name)

from twitch import get_notifications
import asyncio
from discord.ext.tasks import loop

print("Twitch API ist geladen")
@loop(seconds=90)
async def check_twitch_online_streamers():
    channel = client.get_channel(760548853208055871)
    if not channel:
        return

    notifications = get_notifications()
    for notification in notifications:
        await channel.send("@everyone Feuerball07 ist nun live auf Twitch, schaut gerne vorbei! <3 https://www.twitch.tv/feuerball07")
        print("Feuerball07 ist nun online")


with open("config.json") as config:
    config = json.load(config)

#------------------------------------------------Slash Commands----------------------------------------------------------

@tree.command(name="pingfb07", description="Ping den FeuerBot.")
async def ping(int: discord.Interaction):    
    await int.response.send_message("FeuerBot ist online!")

@tree.command(name="info", description="Infos über den FeuerBot.")
async def info(int: discord.Interaction):    
    await int.response.send_message("Ich bin der persönliche Bot des Feuerball07 Servers. Ich befinde mich momentan in der Beta und werde ständig aktualisiert.")

@tree.command(name="twitch", description="Link zu meinem Twitch Kanal")
async def twitch(int: discord.Interaction):    
    await int.response.send_message("https://www.twitch.tv/feuerball07")

@tree.command(name="help", description="Hilfe über den Bot und den Server")
async def help(int: discord.Interaction):    
    await int.response.send_message("'!pingfb07' --> So kannst du sehen, ob ich online bin \n '!twitch' --> Ich schicke den Link von Tims Twitch Channel \n '!info' --> Einige Informationen über mich")

@tree.command(name="say", description="Lasse mich etwas schreiben!")
@app_commands.describe(inhalt = "Was soll ich schreiben?")
@has_permissions(kick_members=True)
async def say(int: discord.Interaction, inhalt: str):
  await int.response.send_message(f"{inhalt}")

#@tree.command(name="stop", description="Stoppe den Server")
#@has_permissions(administrator=True)
#async def slash_command(int:discord.Interaction):
#  await int.response.send_message("Der Bot wird beendet.")
#  await client.close()
#  await user_log.info(f"Bot wurde durch User beendet")

#------------------------------------------------Join/Leave MSG----------------------------------------------------------
  
@client.event
async def on_member_join(member):
    guild = member.guild
    stat = client.get_channel(1073291839806898287)
    await stat.edit(name = f"Mitglieder: {guild.member_count}")
    channel = client.get_channel(760549039602925598)
    await channel.send(f"Hey {member.mention}! Willkommen auf dem Feuerball Server!")
    await user_log.info(f"{member} ist dem Server gejoined")
  
@client.event
async def on_member_remove(member):
    guild = member.guild
    stat = client.get_channel(1073291839806898287)
    await stat.edit(name = f"Mitglieder: {guild.member_count}")
    channel = client.get_channel(760549099656314920)
    await channel.send(f"{member.mention} hat den Server verlassen. Wir werden dich vermissen!")
    await user_log.info(f"{member} hat den Server verlassen")

#---------------------------------------------------Commands-------------------------------------------------------------

private_messages = []

@client.event
async def on_message(message):
    if message.content.startswith("!pingfb07"):
        await message.channel.send("FeuerBot ist online")
    if message.content.startswith("!twitch"):
        link = "https://www.twitch.tv/feuerball07"
        await message.channel.send(link)
    if message.content.startswith("!info"):
        await message.channel.send("Ich bin der persönliche Bot des Feuerball07 Servers. Ich befinde mich momentan in der Beta und werde ständig aktualisiert.")
    if message.content.startswith("!help"):
      await message.channel.send("'!pingfb07' --> So kannst du sehen, ob ich online bin \n '!twitch' --> Ich schicke den Link von Tims Twitch Channel \n '!info' --> Einige Informationen über mich")
#    if message.content.startswith("!clearchat"):
#        if message.author.guild_permissions.manage_messages:
#            async for msg in message.channel.history(limit=100):
#                await msg.delete()
#            await message.channel.send("Chat erfolgreich gelöscht.")
#        else:
#            await message.channel.send("Dir fehlen die Berechtigung um diesen Befehl auszuführen")
    if message.content.startswith('!stop'):
      if message.author.guild_permissions.ban_members:
        await message.channel.send('Bot wird beendet')
        await client.close()
        await user_log('Bot wurde durch Administratorcommand beendet')
    if message.content.startswith('willkommenadminmsg'):
        await message.channel.send('Hey! Ich bin der neue Bot des Feuerball Servers. Infos über mich und meine commands kriegt ihr über !info oder !help.')
    if message.content.startswith('wartungsarbeitadmin'):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Wartungsarbeiten"))
        await message.channel.send("Ich befinde mich nun in Wartungsarbeiten")
        await user_log.info(f"{message.author} hat den Wartungsarbeit Modus eingestellt.")
    if message.content.startswith('wartungsarbeitstop'):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=last_activity))
        await message.channel.send("Wartungsarbeiten wurden beendet")
        await user_log.info(f"{message.author} hat den Wartungsarbeit Modus beendet.")
    if message.content.startswith("!botlog"):
      if message.author.guild_permissions.ban_members:
            with open("bot.log", "rb") as f:
              await message.author.send(file=discord.File(f))
              await message.channel.send("Ich habe dir die Bot-Log Datei per Privatnachricht geschickt! Wenn du die User-Log Datei meintest versuche !userlog")
              await user_log.info(f"{message.author} hat sich die Bot-Log Datei schicken lassen.")
      else:
          await message.channel.send("Du hast keine Berechtigung diesen Command auszuführen.")
    if message.content.startswith("!userlog"):
      if message.author.guild_permissions.ban_members:
            with open("user.log", "rb") as f:
              await message.author.send(file=discord.File(f))
              await message.channel.send("Ich habe dir die User-Log Datei per Privatnachricht geschickt! Wenn du die Bot-Log Datei meintest versuche !botlog")
              await user_log.info(f"{message.author} hat sich die User-Log Datei schicken lassen.")
      else:
          await message.channel.send("Du hast keine Berechtigung diesen Command auszuführen.")
    if message.content.startswith("!activitychange"):
      if os.path.exists("last_activity.txt"):
         with open("last_activity.txt", "r") as f:
           last_activity = f.read()
           await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=last_activity))
    if message.content.startswith("!betalogs"):
      if message.author.guild_permissions.ban_members:
        with open("betalogs.txt", "r") as file:
            content = file.read()
        await message.channel.send(content)
    
#-------------------------------------------------Bot Actions------------------------------------------------------------
        
    if message.author == client.user:
        return
    if message.channel.type == discord.ChannelType.private:
        private_messages.append(message.content)
        print(f"Private Nachricht von {message.author} empfangen: {message.content}")
        user_log.info(f"Private Nachricht von {message.author} empfangen: {message.content}")
        channel = client.get_channel(1066754831303323648)
        await channel.send(f"Private Nachricht von {message.author} empfangen: {message.content}")   

keep_alive()
try:
  client.run(os.getenv("API-Key"))
except:
    os.system("kill 1")

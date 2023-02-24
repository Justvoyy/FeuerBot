#Write it in your on_ready function
client.add_view((Ticket))

createdchannel = None

class Ticket(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(emoji="Emoji <name:id>", style=discord.ButtonStyle.green, custom_id='button')
  async def supportbutton(self, int: discord.Interaction, button: discord.ui.Button):
    if button.custom_id == 'button':
      guild = int.guild
      category = discord.utils.get(int.guild.categories, id = 760552306563088465)
      creator = int.user.name
      ticketcreator = int.user
      global userid
      userid = int.user
      global createdchannel
      createdchannel = await guild.create_text_channel(f"Ticket von {creator}", category=category)
      id = 1009514983471714437 #Id of the support role
      support = discord.utils.get(guild.roles, id = id)
      await createdchannel.set_permissions(int.guild.get_role(int.guild.id),
      view_channel=False,
      send_messages=False,
      read_messages=False)
      await createdchannel.set_permissions(ticketcreator,
      view_channel=True,
      send_messages=True,
      read_messages=True,
      add_reactions=True,
      embed_links=True,
      attach_files=True,
      read_message_history=True,
      external_emojis=True)
      await createdchannel.set_permissions(support,
      view_channel=True,
      send_messages=True,
      read_messages=True,
      add_reactions=True,
      embed_links=True,
      attach_files=True,
      read_message_history=True,
      external_emojis=True,
      manage_messages=True)
      user_log.info(f"{creator} hat ein Support Ticket erstellt")
      alert = client.get_channel(1002868312604160051)
      await alert.send(f"@here {creator} hat ein Ticket erstellt!")
      await createdchannel.send(f"Hallo {int.user.mention}! Bitte habe Geduld, der Support wurde benachrichtigt und wird gleich bei dir sein.")
      await int.message.edit(view=self)

@tree.command(name="sendticketbutton", description="...")
@has_permissions(administrator=True)
@app_commands.guild_only()
async def ticketbutton(int: discord.Interaction):
  col = 0x680204 #Color of the embed message
  embed = discord.Embed(
  title = "Support Ticket",
  description = "Interagiere mit <:Hiiiilfeee:839066333689675808>, um ein Support Ticket zu öffnen",
  color = col)
  view = Ticket()
  await int.channel.send(embed=embed, view=view)
  
# Ticket commands if you dont want to use the Button
  
userid = None

@tree.command(name="support", description="Erstelle ein Support Ticket")
@app_commands.describe(problem="Erkläre dein Problem, damit wir dir schnellstmöglich helfen können.")
@app_commands.guild_only()
async def createticket(int: discord.Interaction, problem: str):
  await int.response.send_message(f"{int.user.mention} dein Ticket wurde erstellt.", ephemeral=True)
  guild = int.guild
  category = discord.utils.get(int.guild.categories, id = 760552306563088465)
  creator = int.user.name
  ticketcreator = int.user
  global userid
  userid = int.user
  with open("ticketcreator.txt", "w") as f:
            f.write(f"{creator}")
  createdchannel = await guild.create_text_channel(f"Ticket von {creator}", category=category)
  id = 1009514983471714437
  support = discord.utils.get(guild.roles, id = id)
  await createdchannel.set_permissions(int.guild.get_role(int.guild.id),
  view_channel=False,
  send_messages=False,
  read_messages=False)
  await createdchannel.set_permissions(ticketcreator,
  view_channel=True,
  send_messages=True,
  read_messages=True,
  add_reactions=True,
  embed_links=True,
  attach_files=True,
  read_message_history=True,
  external_emojis=True)
  await createdchannel.set_permissions(support,
  view_channel=True,
  send_messages=True,
  read_messages=True,
  add_reactions=True,
  embed_links=True,
  attach_files=True,
  read_message_history=True,
  external_emojis=True,
  manage_messages=True)
  user_log.info(f"{creator} hat ein Support Ticket mit dem Grund : {problem}")
  alert = client.get_channel(1002868312604160051)
  await alert.send(f"@here {creator} hat ein Ticket erstellt mit dem Grund : {problem}")
  await createdchannel.send(f"Hallo {int.user.mention}! Bitte habe Geduld, der Support wurde benachrichtigt und wird gleich bei dir sein.")

@tree.command(name="closeticket", description="Schließe das aktuelle Ticket und verschiebe es in die Kategorie Closed Tickets")
@app_commands.describe(grund="Warum wurde das Ticket geschlossen?")
@app_commands.guild_only()
async def closeticket(int: discord.Interaction, grund: str):
  guild = int.guild
  alert = client.get_channel(1002868312604160051)
  creator = int.user.name
  supportchannel = int.channel_id
  closechannel = int.channel
  if closechannel.name.startswith('ticket'):
    ticketchannel = client.get_channel(supportchannel)
    closedticketscat = discord.utils.get(int.guild.categories, id=1002869496480010270)
    await int.response.send_message(f"Das Ticket wird nun von dir mit folgendem Grund geschlossen: {grund}", ephemeral=True)
    await ticketchannel.send(f"Das Ticket wird nun geschlossen!")
    global userid
    await alert.send(f'Das Ticket wurde durch {creator} mit dem Grund: "{grund}" geschlossen!')
    await int.channel.edit(category=closedticketscat)
    await ticketchannel.set_permissions(userid,
    view_channel=False,
    send_messages=False,
    read_messages=False,
    add_reactions=False,
    embed_links=False,
    attach_files=False,
    read_message_history=False,
    external_emojis=False)
  else:
    await int.response.send_message(f"Diesen Channel kannst du nicht schließen.")
    user_log.info(f"{int.user} wollte einen Standard-Channel schließen")
    await alert.send(f"{creator} wollte einen Standard-Channel schließen")

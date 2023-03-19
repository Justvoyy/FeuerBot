@tree.command(name="file", description="Sends a file of the Server.")
@app_commands.choices(datei=[
    app_commands.Choice(name="Sends the Bot-Log File", value="Botlog"),
    app_commands.Choice(name="Sends the User-Log File", value="Userlog")
    ])
@app_commands.guild_only()
@has_permissions(ban_members=True)
async def file(int: discord.Interaction, datei: app_commands.Choice[str]):
  Botlog = "bot.log"
  Userlog = "user.log"
  if (datei.value == 'Botlog'):
    with open("bot.log", "rb") as f:
      private = await int.user.create_dm()
      await private.send(file=discord.File(f))
      await int.response.send_message("I send you the Bot-Log File. If you wanted the Userlog try /file Userlog", ephemeral=True)
      user_log.info(f"{int.user} used /file.")
  elif (datei.value == 'Userlog'):
    with open("user.log", "rb") as f:
      private = await int.user.create_dm()
      await private.send(file=discord.File(f))
      await int.response.send_message("I send you the User-Log File. If you wanted the Userlog try /file Bot", ephemeral=True)
      user_log.info(f"{int.user} used /file.")

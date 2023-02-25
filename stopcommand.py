@tree.command(name="stop", description="Stoppe den Server")
@has_permissions(administrator=True)
@app_commands.guild_only()
async def stopcommand(int:discord.Interaction):
  await int.response.send_message("Der Bot wird beendet.")
  user_log.info(f"Bot wurde durch {int.user} beendet")
  log = client.get_channel(1066754831303323648)
  await log.send(f"Bot wurde durch {int.user} beendet")
  await client.close()

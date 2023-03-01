@tree.command(name="stop", description="Stoppe den Server")
@has_permissions(administrator=True)
@app_commands.guild_only()
async def stopcommand(int:discord.Interaction):
  await int.response.send_message("Bot will be closed")
  user_log.info(f"Bot got closed by {int.user}")
  log = client.get_channel(1066754831303323648)
  await log.send(f"Bot got closed by {int.user}")
  await client.close()

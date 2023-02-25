@tree.command(name="embed", description="Send an embed message")
@app_commands.describe(titel = "What should be the title?")
@app_commands.describe(describe="What should be the description?")
@app_commands.guild_only() #Only useable on Guilds
@has_permissions(ban_members=True) #Only for Mods (with Ban Perms)
async def embed(int: discord.Interaction, titel: str, describe: str):
  col = 0x680204 #Could be any color you want
  embed = discord.Embed(
  title = titel,
  description = describe,
  color = col,
  timestamp = datetime.datetime.now())
  await int.channel.send(embed=embed)

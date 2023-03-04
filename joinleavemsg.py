@client.event
async def on_member_join(member):
    guild = member.guild
    stat = client.get_channel(1073291839806898287)
    await stat.edit(name = f"Members: {guild.member_count}")
    channel = client.get_channel(760549039602925598)
    await channel.send(f"Hey {member.mention}! Welcome on ...")
    await user_log.info(f"{member} joined the server!")
  
@client.event
async def on_member_remove(member):
    guild = member.guild
    stat = client.get_channel(1073291839806898287)
    await stat.edit(name = f"Mitglieder: {guild.member_count}")
    channel = client.get_channel(760549099656314920)
    await channel.send(f"{member} left the server!")
    await user_log.info(f"{member} left the server!")

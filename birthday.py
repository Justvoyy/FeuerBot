with open('birthdays.json', 'r') as f:
  birthdays = json.load(f)

def save_birthday(name, date, day, month):
    with open("birthdays.json", "r+") as f:
        daten = json.load(f)
        daten[str(name)] = {"day": day, "month": month}
        json.dump(daten, f)
  
def check_birthdays():
  today = datetime.now().strftime("%m-%d")
  for name, date in birthdays.items():
      if date == today:
        birthday_channel = client.get_channel(760547543976378398)
        birthday_channel.send(f"Happy birthday, {name}!")
  return

@tree.command(name="add_birthday", description="Save your Birthday!")
@app_commands.describe(day = "Day (without 0 before)")
@app_commands.describe(month= "Month (without 0 before)")
@app_commands.guild_only()
async def add_birthday(interaction: discord.Interaction, day: str, month: str):
  month = int(month)
  day = int(day)
  try:
    if month > 13 or month < 1:
                await interaction.repsonse.send_message('Month must be between 13 and 1')
                return
    else:
                pass
    if month in (1, 3, 5, 7, 8, 10, 12):
                if day > 31 or day < 1:
                    await interaction.response.send_message('Date is not correct!')
                    return
                else:
                    pass
    elif month in (4, 6, 9, 11):
                if day > 30 or day < 1:
                    await interaction.response.send_message('Date is not correct!
                    return
                else:
                    pass
    elif month == 2:
                if day > 29 or day < 1:
                    await interaction.response.send_message('Date is not correct!')
                    return
                else:
                    pass
    else:
                await interaction.response.send_message('Date is not correct!')
                return
  except:
            await interaction.response.send_message("Error!")
            return
    
  name = str(interaction.user.id)
  date = f"{day}.{month}"
  save_birthday(name, date, day, month)
  await interaction.response.send_message(f"Saved your Birhtday: {date}")

@loop(hours=1)
async def loop_check_birthdays():
  today = datetime.now()
  with open('birthdays.json', 'r') as f:
    data = json.load(f)
    gratulated_today = []
    for name, values in data.items():
      day = values["day"]
      month = values["month"]
      geburtstag = datetime(today.year, month, day)
      if geburtstag.date() == today.date() and name not in gratulated_today:
        birthday_channel = client.get_channel(760547543976378398)
        user = await client.fetch_user(name)
        await birthday_channel.send(f"Happy birhtday, {user.mention}!")
        gratulated_today.append(name)
      return

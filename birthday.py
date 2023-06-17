with open('geburtstage.json', 'r') as f:
  birthdays = json.load(f)

def save_birthday(name: str, date: str, tag: int, monat: int):
  with open("geburtstage.json", "r+") as f:
    daten = json.load(f)
    daten[str(name)] = {"tag": tag, "monat": monat}
    f.seek(0)
    json.dump(daten, f)
  
def check_birthdays():
  today = datetime.now().strftime("%m-%d")
  for name, date in birthdays.items():
      if date == today:
        birthday_channel = client.get_channel(760547543976378398)
        birthday_channel.send(f"Herzlichen Glückwunsch zum Geburtstag, {name}!")
  return

@tree.command(name="geburtstag", description="Speicher deinen Geburtstag ab und wir gratulieren dir!")
@app_commands.describe(tag = "Tag (ohne 0 vor einstelligen Zahlen)")
@app_commands.describe(monat= "Monat (ohne 0 vor einstelligne Zahlen)")
@app_commands.guild_only()
async def add_birthday(interaction: discord.Interaction, tag: str, monat: str):
  monat = int(monat)
  tag = int(tag)
  try:
    if monat > 13 or monat < 1:
                await interaction.repsonse.send_message('Monat muss zwischen 12 und 1 sein')
                return
    else:
                pass
    if monat in (1, 3, 5, 7, 8, 10, 12):
                if tag > 31 or tag < 1:
                    await interaction.response.send_message('Datum nicht korrekt!')
                    return
                else:
                    pass
    elif monat in (4, 6, 9, 11):
                if tag > 30 or tag < 1:
                    await interaction.response.send_message('Datum nicht korrekt!')
                    return
                else:
                    pass
    elif monat == 2:
                if tag > 29 or tag < 1:
                    await interaction.response.send_message('Datum nicht korrekt!')
                    return
                else:
                    pass
    else:
                await interaction.response.send_message('Versuche es nochmal!')
                return
  except:
            await interaction.response.send_message("Fehler aufgetreten!")
            return
    
  name = str(interaction.user.id)
  date = f"{tag}.{monat}"
  with open('geburtstage.json', 'r') as f:
    birthdays = json.load(f)
  if name in birthdays:
    await interaction.response.send_message("Dein Geburtstag ist bereits gespeichert verwende /geburtstag-löschen um ihn zu entfernen.")
  else:
    save_birthday(name, date, tag, monat)
    await interaction.response.send_message(f"Dein Geburtstag wurde am {date} gespeichert!")

@loop(hours=12)
async def loop_check_birthdays():
    print("Geburtstage werden geprüft!")
    bot_log.info("Geburtstage werden geprüft")
    today = datetime.now()
    with open('geburtstage.json', 'r') as f:
        data = json.load(f)
    gratulated_today = []
     def check_gratulated(name):
      with open("gratulated.txt", "r") as f:
        gratulated_names = f.read()
      return name in gratulated_names
    for name, values in data.items():
        tag = values["tag"]
        monat = values["monat"]
        geburtstag = datetime(today.year, monat, tag)
        if geburtstag.date() == today.date() and name not in gratulated_today and not check_gratulated(name):
            birthday_channel = client.get_channel(760547543976378398)
            user = await client.fetch_user(name)
            await birthday_channel.send(f"Herzlichen Glückwunsch zum Geburtstag, {user.mention}!")
            gratulated_today.append(name)
            with open("gratulated.txt", "w") as f:
              f.write(f"{name}"


@tree.command(name="geburtstag-löschen", description="Lösche deinen Geburtstag aus der Datenbank")
async def del_birthday(int: discord.Interaction):
  id = int.user.id
  with open('geburtstage.json', 'r') as f:
    birthdays = json.load(f)
  if str(id) in birthdays:
    del birthdays[str(id)]
    with open("geburtstage.json", "w") as f:
      json.dump(birthdays, f)
    await int.response.send_message("Dein Geburtstag wurde erfolgreich gelöscht!")
  else:
    await int.response.send_message("Dein Geburtstag konnte nicht gefunden werden!")

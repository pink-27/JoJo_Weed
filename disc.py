import discord
import os
client = discord.Client()
@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  if message.content.startswith('+hello'):
    await message.channel.send('Sup shawty!')

client.run(os.getenv('TOKEN'))

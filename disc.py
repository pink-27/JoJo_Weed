import discord
import os
import requests
import json
import random
import ast
from replit import db
client = discord.Client()



jojo = ['jojo', 'i hate you jojo', 'dio', 'giorno', 'joestar', 'mista', 'golden wind', 'star platinum']


jojo_ref=['And that’s why I turned one of your pistols into a banana. It’s your last meal. Take your time… enjoy it.', 'DIO… I don’t understand why you’re so loyal to him. Are you honestly telling me… that you’d die for him?', 'You are such a thoughtful boy, JoJo.', 'A dad should give his son an allowance, right?', 'Hold it! I still have the right to raise… I raise you my mother’s soul.' 'Jojo, being human means having limits. I’ve learned something. The more carefully you scheme, the more unexpected events come along.']


def update_jojo_ref(jojo_thing):
  if "jojos" in db.keys():
    jojos = db["jojos"]
    jojos.append(jojo_thing)
    db["jojos"]=jojos
  else:
    db["jojos"] = [jojo_thing]

def delete(index):
  jojos = db["jojos"]
  if len(jojos)>index:
    del jojos[index]
    db["jojos"]=jojos



@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):

    if message.author==client.user:
        return
    if message.content.startswith('+hello'):
        await message.channel.send('Sup shawty!')
    options = jojo_ref
    if "jojos" in db.keys():
      options.extend(db["jojos"])
    if any(word in message.content for word in jojo):
        await message.channel.send(random.choice(options))
    if message.content.startswith('+newref'):
        jojo_things = message.content.split("+newref ", 1)[1]
        update_jojo_ref(jojo_things) 
        await message.channel.send("new jojo reference has sucesfully been added!")
    if message.content.startswith('+delref'):
      jojos = []
      if "jojos" in db.keys():
        index = int(message.content.split('+delref', 1)[1])
        delete(index)
        jojos = db["jojos"]
        await message.channel.send(jojos)
      
   

client.run(os.getenv('TOKEN'))


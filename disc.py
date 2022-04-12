import discord
import os
import requests
import json
import random
import ast
from discord.ext import commands
from replit import db
import datetime
import nacl
import time


client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


'''
jojo = ['jojo', 'i hate you jojo', 'dio', 'giorno', 'joestar', 'mista', 'golden wind', 'star platinum']


jojo_ref=['And that’s why I turned one of your pistols into a banana. It’s your last meal. Take your time… enjoy it.', 'DIO… I don’t understand why you’re so loyal to him. Are you honestly telling me… that you’d die for him?', 'You are such a thoughtful boy, JoJo.', 'A dad should give his son an allowance, right?', 'Hold it! I still have the right to raise… I raise you my mother’s soul.' 'Jojo, being human means having limits. I’ve learned something. The more carefully you scheme, the more unexpected events come along.']

if "responding" not in db.keys():
  db["responding"]=True


def update_jojo_ref(jojo_thing):
  if "jojos" in db.keys():
    jojos = db["jojos"]
    jojos.append(jojo_thing)
    db["jojos"]=jojos
  else:
    db["jojos"] = [jojo_thing]

#def create_tag(name, cont):
  

def delete(index):
  jojos = db["jojos"]
  if len(jojos)>index:
    del jojos[index]
    db["jojos"]=jojos

'''


'''
@client.event
async def on_message(message):

    if message.author==client.user:
        return
    if message.content.startswith('+hello'):
        await message.channel.send('Sup shawty!')
    if db["responding"]:
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
    if message.content.startswith('+list'):  
      jojos = []
      if "jojos" in db.keys():
        jojos = db["jojos"]
      await message.channel.send(f'jojo ref= {jojos.value}')
      await message.channel.send(f'jojo triggers= {jojo}')
    if message.content.startswith('+respond'):
      response = message.content.split('+respond ', 1)[1]
      if response.lower()=='true':
        db["responding"]=True
        await message.channel.send('now the bot is active')
      elif response.lower()=='false':
        db["responding"]=False
        await message.channel.send('now the bot is shut down')
'''

start_time = 0
end_time = 0

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.command()
async def urmom(ctx):
  res = requests.get("https://api.yomomma.info/")
  data = res.json()
  tmp = discord.Embed(title = data["joke"] , color = 0x696969)
  await ctx.reply(embed = tmp, mention_author = True)

  
@client.command()
async def join(ctx):
  global start_time
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
    start_time = datetime.datetime.now()
  else:
    await ctx.send("I am terribly sorry, but I cannot join you as you are not in a voice channel.")

@client.command()
async def leave(ctx):
  global end_time
  global start_time
  if (ctx.author.voice):
    end_time = datetime.datetime.now()
    delta = end_time-start_time
    
    await ctx.send( f"you left the vc, {delta.seconds}s were spent studying")
    await ctx.voice_client.disconnect()
    
    
  else:
    await ctx.send("you need to join one vc b4 leaving one daaaa.")
    
  


@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")



client.run(os.getenv('TOKEN'))


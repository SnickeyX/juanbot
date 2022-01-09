import discord, os, requests
import json 
import asyncio 
from datetime import datetime 
from discord.ext import commands, tasks
from random import randint 

bot = commands.Bot(command_prefix ="$", activity = discord.Activity(type=discord.ActivityType.listening, name="lil nas x"))

def get_quote():
          response = requests.get("https://zenquotes.io/api/random")
          json_data = json.loads(response.text)
          quote = json_data[0]['q'] + " -" + json_data[0]['a']
          return quote 
          
          
def get_poke():
          response1 = requests.get("https://pokeapi.co/api/v2/pokemon/") #getting the latest number of pokemons
          ini_json_data = json.loads(response1.text)
          poke_number = ini_json_data["count"]
          poke_id = randint(0,poke_number)
          response2 = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(poke_id)) #getting info about that pokemon 
          json_data = json.loads(response2.text)
          pokemon = json_data["forms"][0]["name"]
          return pokemon 

@bot.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event 
async def on_message(message):


  if message.content.startswith('hello?'):
      await message.reply('Hello!')

  if message.content.startswith('quote?'):
      quote = get_quote()
      await message.reply(quote)

  await bot.process_commands(message)


@bot.command(name = "marco",            
            help= "will it really polo?",
	          brief="Prints polo back to the channel.")
async def marco(ctx):
	await ctx.reply("polo")


@bot.command(name = "whatpokemonami",
             help = "find out what pokemon you are!",
             breif = "let's you know what pokemon you are.")
async def whatpokemonami(ctx):
	await ctx.reply(get_poke())

@bot.command(name = "date?",
             help = "find out what the current date and time are",
             breif = "provides current date and time in dd/mm/yyyy H:M:S format.")
async def today(ctx):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  await ctx.reply(dt_string)

@bot.command(name = "remind",
             help = "command to set a reminder, accepted units are s,m,h,d. e.g $remind 5s {some_task}",
             brief = "set a reminder!")
async def remind(ctx, time, task): 
  def convert(time):
    pos = ['s', 'm', 'h', 'd']

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

    unit = time[-1]

    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    
    return val * time_dict[unit]
 
  converted_time = convert(time)

  if converted_time == -1: 
    await ctx.channel.send("Invalid unit used")
    return

  if converted_time == -2: 
    await ctx.channel.send("Please use integers for time")
    return 
  
  await ctx.channel.send(f'Reminder started for **{task}** and will alert in **{time}**')

  await asyncio.sleep(converted_time)
  await ctx.send(f'{ctx.author.mention}, your reminder for **{task}** is finished!')


@bot.command(name = "guess",
             help = "a simple number guessing game, try your luck!",
             brief = "number guessing ")
async def guess(ctx):
  await ctx.reply('Guess a number between 1 and 10.')

  def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

  answer = randint(0,10)

  try:
      msg = await bot.wait_for("message", check=check,timeout = 5)
  except asyncio.TimeoutError:
      return await ctx.send(f'Sorry, you took too long it was {answer}.')

  if msg.content == answer:
      await ctx.reply("You got it! \U0001F60E")
  else:
      await ctx.reply(f'Oops \U0001F62D. It is actually {answer}.')

#setting a reminder system for particular days
@tasks.loop(hours = 6) 
async def alarm():
    message_channel = bot.get_channel(925834088957476925)
    print(f"Got channel {message_channel}")
    await message_channel.send("insert_reminder")
  

@alarm.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

if (datetime.today().strftime("%A") == "Tuesday"):
  alarm.start()

bot.run(os.getenv('TOKEN'))
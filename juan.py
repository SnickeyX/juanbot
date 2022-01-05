import discord, os, requests
import json 
#import asyncio 
from discord.ext import commands
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

  if message.content.startswith('whatpokemonami?'):
      pokemon = get_poke()
      await message.reply(pokemon)


  await bot.process_commands(message)


@bot.command(name = "ping")
async def ping(ctx):
	await ctx.channel.send("pong")


bot.run(os.getenv('TOKEN'))
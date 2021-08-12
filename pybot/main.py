import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
bot = commands.Bot(command_prefix='$')


@bot.command()
async def money(ctx, *args):
    apiurl = 'https://api.coinbase.com/v2/prices/{}-{}/{}'
    apiargs = {'base':'BTC', 'to':'USD', 'buyorsell':'buy'}

    if(len(args) == 1):
        apiargs['base'] = args[0]
    
    elif(len(args) == 2):
        apiargs['base'] = args[0]
        apiargs['to'] = args[1]

    r = requests.get(apiurl.format(apiargs.get('base'), apiargs.get('to'), apiargs.get('buyorsell')))

    if(r.status_code == 200):
        r = r.json().get('data')
        await ctx.send(r.get('base') + " -> " + r.get('currency')
              + " " + r.get('amount'))

    else:
        await ctx.send("You messed up dummy!")

@bot.command()
async def buy(ctx, arg):
    r = requests.get('https://api.coinbase.com/v2/prices/{}-USD/buy'.format(arg))
    if(r.status_code == 200):
        r = r.json().get('data')
        await ctx.send(r.get('base') + " -> " + r.get('currency')
                + " $" + r.get('amount'))

    else:
        await ctx.send("You messed up dummy!")

@bot.command()
async def sell(ctx, arg):
    r = requests.get('https://api.coinbase.com/v2/prices/{}-USD/sell'.format(arg))
    if(r.status_code == 200):
        r = r.json().get('data')
        await ctx.send(r.get('base') + " -> " + r.get('currency')
                + " $" + r.get('amount'))

    else:
        await ctx.send("You messed up dummy!")


@bot.event
async def on_ready():
    print('----BOT READY----')

bot.run(os.getenv('TOKEN'))

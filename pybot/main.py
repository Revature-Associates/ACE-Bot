import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
bot = commands.Bot(command_prefix='$')


async def msg_currency(ctx, api_request):
    r = requests.get(api_request)

    if(r.status_code == 200):
        r = r.json().get('data')
        await ctx.send(r.get('base') + " -> " + r.get('currency')
              + " " + r.get('amount'))

    else:
        await ctx.send("You messed up dummy!")

@bot.command()
async def money(ctx, *args):
    apiurl = 'https://api.coinbase.com/v2/prices/{}-{}/{}'
    apiargs = {'base':'BTC', 'to':'USD', 'buyorsell':'buy'}

    if(len(args) == 1):
        apiargs['base'] = args[0]
    
    elif(len(args) == 2):
        apiargs['base'] = args[0]
        apiargs['to'] = args[1]
    
    await msg_currency(ctx, apiurl.format(apiargs.get('base'), apiargs.get('to'), apiargs.get('buyorsell')))

@bot.command()
async def buy(ctx, arg):
    await msg_currency(ctx, 'https://api.coinbase.com/v2/prices/{}-USD/buy'.format(arg))

@bot.command()
async def sell(ctx, arg):
    await msg_currency(ctx, 'https://api.coinbase.com/v2/prices/{}-USD/sell'.format(arg))


@bot.event
async def on_ready():
    print('----BOT READY----')

bot.run(os.getenv('TOKEN'))

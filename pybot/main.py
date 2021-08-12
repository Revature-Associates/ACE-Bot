import os
import discord
import requests
from dotenv import load_dotenv
import logging

load_dotenv()
client = discord.Client()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Howdy! :cowboy:')

    if message.content.startswith('$money'):
        btc = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy') \
            .json().get('data')
        await message.channel.send(
            btc.get('base') + " -> " + btc.get('currency')
            + " $" + btc.get('amount'))
        eth = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy') \
            .json().get('data')
        await message.channel.send(
            eth.get('base') + " -> " + eth.get('currency')
            + " $" + eth.get('amount'))

    if message.content.startswith('$buy '):
        symbol = message.content.split(' ')
        r = requests.get('https://api.coinbase.com/v2/prices/'+symbol[1]+'-USD/buy') \
            .json().get('data')
        await message.channel.send(
            r.get('base') + " -> " + r.get('currency')
            + " $" + r.get('amount'))

    if message.content.startswith('$sell '):
        symbol = message.content.split(' ')
        r = requests.get('https://api.coinbase.com/v2/prices/'+symbol[1]+'-USD/sell') \
            .json().get('data')
        await message.channel.send(
            r.get('base') + " -> " + r.get('currency')
            + " $" + r.get('amount'))

client.run(os.getenv('TOKEN'))

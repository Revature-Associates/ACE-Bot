import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


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
        r = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy') \
            .json().get('data')
        await message.channel.send(
            r.get('base') + " -> " + r.get('currency')
            + " $" + r.get('amount'))

client.run(os.getenv('TOKEN'))

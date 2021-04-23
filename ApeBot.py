import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=commands.when_mentioned_or("$"),
                   description='Apes to the moon!')

@client.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(client.user))
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('ape'):
        await message.channel.send('Apes hodl to the moon!')




client.run(token)
import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv
from stonk import Stonk

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=commands.when_mentioned_or("$"),
                   description='Apes to the moon!')

stonk = Stonk(client)

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

    await client.process_commands(message)

client.add_cog(stonk)
client.run(token)
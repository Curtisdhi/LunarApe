import os
import sys
import signal
import asyncio
import discord
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv
from stonk import Stonk

def setupPersistence():
    con = sqlite3.connect('stonks.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS watch_list (channel_id int, name text, symbols text)")
    
    con.commit()
    con.close()



load_dotenv()

if len(sys.argv) > 1 and sys.argv[1].strip().lower() == 'prod':
    token = os.getenv('DISCORD_TOKEN') 
else:
    token = os.getenv('DEV_DISCORD_TOKEN')

setupPersistence()

client = commands.Bot(command_prefix=commands.when_mentioned_or("$"), description='Apes to the moon!')

#handles Ctrl+Z more cleanly
def handler(signum, frame):
    print('Apebot heading to the moon!')
    client.close()
    exit()

signal.signal(signal.SIGTSTP, handler)

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
    
stonk = Stonk(client)
client.add_cog(stonk)
client.run(token)
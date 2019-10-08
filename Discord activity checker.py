# All imports needed to run this
import discord
from discord.ext import commands,tasks
from discord.utils import get
from bs4 import BeautifulSoup
import random
import requests
from datetime import datetime
from async_timeout import asyncio

# You can change the prefix to anything (currently //)
client = commands.Bot(command_prefix = '//')

# This is the time messages will be send out (local time)
send_time='12:00'

# Just a message for the command line to check if it is online
@client.event
async def on_ready():
    print(f'{client.user.name} is online')

# Simple test to see if the bot works (//test)
@client.command()
async def test(ctx):
    await ctx.send(f'Test succeeded within {round(client.latency * 1000)}ms')

# Here it will scrape DayZRP site
async def time_check():
    # Wait till client is ready
    await client.wait_until_ready()
    # Put your channel id in here
    # TODO: Inserting channel id where you want to send it (just numbers no " ' ")
    channel = client.get_channel('CHANNEL ID HERE')
    while not client.is_closed():
        # Checking current time
        now = datetime.strftime(datetime.now(), '%H:%M')
        # Checking if current time is equal to time it need to send
        if now == send_time:
            # Deleting first (currently 20) messages
            async for message in channel.history(limit=20):
                await discord.Message.delete(message)
            # Insert link to grouppage here
            # TODO: Insert link to your group here (https://www.dayzrp.com/groups/)
            site = 'INSERT LINK TO WEBSITE'
            # Just some scraper things
            html = requests.get(site, headers={'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}).content
            soup = BeautifulSoup(html, "html.parser")

            # Find all photo containers
            containers = soup.findAll('a',{'class':'ipsUserPhoto_mini'})
            
            # Scraping info from site
            for container in containers:
                alt = container.img['alt']
                url = container.img['src']
                prof = container['href']

                # Going to their profile
                html = requests.get(prof, headers={'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}).content
                soup = BeautifulSoup(html, "html.parser")
                # Getting info from profile
                containera = soup.findAll('span',{'class':'ipsDataItem_generic'})

                # Getting last online
                time = containera[3].text

                # Making a discord embed
                value = random.randint(0, 0xffffff)
                embed = discord.Embed(title='User Information', description=f'Profile of {alt}', color=value)
                embed.add_field(name='Name:', value=alt, inline=True)
                embed.add_field(name='Last played:', value=time, inline=True)
                embed.set_thumbnail(url=url)
                # Sending the message
                await channel.send(embed=embed)
            # If succeeded wait 60 seconds (so it doesnt happen again)
            tijd = 60
        else:
            # Try again if not succeeded
            tijd=1
        # Waiting a certain time
        await asyncio.sleep(tijd)

# Loop to call time_check
client.loop.create_task(time_check())

# Starting the bot
# TODO: Insert own bot code here
client.run('Your Bot Code Here')

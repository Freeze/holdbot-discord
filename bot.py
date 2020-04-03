#!/usr/bin/python3
# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext import commands
import platform
import os
import random
import requests
import json
import time
import datetime

openDotaApiKey = os.getenv('OPENDOTA_API_KEY')
discordToken = os.getenv('DISCORD_BOT_TOKEN')


client = commands.Bot(description="holden sucks at things", command_prefix='!')


f = []

for (path, dirnames, filenames) in os.walk('/memes'):
    f.extend(os.path.join(path, name) for name in filenames)


def stanway():
    url = "https://api.opendota.com/api/players/104423716/matches"
    headers = {
        'api_key': openDotaApiKey,
        'Cache-Control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers)
    rand_match = random.randint(1, 986)
    something = response.json()
    hero_id = something[rand_match]["hero_id"]
    with open('heroes.json') as h:
        data = json.load(h)
    for x in data["result"]["heroes"]:
        if x["id"] == hero_id:
            hero_name = (x['localized_name'])
            kills = str(something[rand_match]["kills"])
            deaths = str(something[rand_match]["deaths"])
            assist = str(something[rand_match]["assists"])
            datee = something[rand_match]["start_time"]
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(datee))
            match_id = str(something[rand_match]["match_id"])
            url2 = "https://api.opendota.com/api/matches/" + match_id
            response2 = requests.request("GET", url2, headers=headers)
            something2 = response2.json()
            for q in something2['players']:
                if q['account_id'] == 104423716:
                    win_result = q['win']
                    if win_result == 1:
                        win_result = "Win!"
                    else:
                        win_result = "Loss."
            stanwayDict = {}
            stanwayDict['kills'] = "**" + kills + "**"
            stanwayDict['hero'] = hero_name
            stanwayDict['deaths'] = "**" + deaths + "**"
            stanwayDict['assist'] = "**" + assist + "**"
            stanwayDict['datee'] = datee
            stanwayDict['date'] = date
            stanwayDict['match_id'] = match_id
            stanwayDict['win_result'] = win_result
            if win_result == "Loss.":
                stanwayDict['result_color'] = 0xFF0000
                stanwayDict['resultText'] = "Big noob.  Lost game."
            else:
                stanwayDict['result_color'] = 0x008000
                stanwayDict['resultText'] = "Stanway carried this game."
            killInt=int(kills)
            deathInt=int(deaths)
            assistInt=int(assist)
            if killInt + assistInt < deathInt:
                stanwayDict['feed'] = "yes"
            else:
                stanwayDict['feed'] = "no"
            stanwayDict['title'] = "Stanway plays " + hero_name
                

            return stanwayDict
            # return("Random Stanway Game of Dota:\n" + hero_name + "\nScore: " + kills + " - " + deaths + " - " + assist + "\nResult: " + win_result + "\nDate: " + date)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # This is buggy, let us know if it doesn't work.
    return await client.change_presence(activity=discord.CustomActivity(name='poopin lol'))
    #return await client.change_presence('💩 !meme 💩')

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def drinky(ctx):
    x = stanway()
    embed = discord.Embed(title=x['title'], color=x['result_color'], timestamp=datetime.datetime.utcfromtimestamp(x['datee']))
    embed.set_thumbnail(url="https://i.imgur.com/w1i15X0.png")
    embed.add_field(name="Date", value=x['date'],inline=False)
    embed.add_field(name="Match ID", value=x['match_id'],inline=False)
    embed.add_field(name="Kills", value=x['kills'], inline=True)
    embed.add_field(name="Deaths", value=x['deaths'], inline=True)
    embed.add_field(name="Assists", value=x['assist'], inline=True)
    embed.add_field(name="Feed?", value=x['feed'])
    embed.set_footer(text=x['resultText'])
    await ctx.send(embed=embed)


@client.command()
async def wut(ctx):
    await ctx.send("lamo")


@client.command()
async def meme(ctx):
    await ctx.send(file=discord.File(f[random.randint(1, 6474)]))


async def on_message(message):
    if message.content.startswith('!die'):
        await client.send_file(message.channel, "/memes/die.png")
    elif message.content.startswith('!boop'):
        await client.send_message(message.channel, "@here Ark Memes????????????")
    elif message.content.startswith('!wtf'):
        await client.send_message(message.channel, message.author.id)
    elif message.author.id == ("206174821963399168"):
        await client.add_reaction(message, "🇬")
        await client.add_reaction(message, "🇦")
        await client.add_reaction(message, "🇾")
    elif message.author.id == ("95842251191652352"):
        lamo = random.randint(1, 15)
        if lamo == 7:
            await client.add_reaction(message, "🇸")
            await client.add_reaction(message, "🇴")
            await client.add_reaction(message, "🇾")

client.run(discordToken)

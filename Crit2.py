# -*- coding: utf-8 -*-
"""
Created on Sun May  8 17:26:14 2022

@author: Haven
"""
import nest_asyncio
nest_asyncio.apply()

# mapBot.py
import os

import discord
from dotenv import load_dotenv
import regex as re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

def damCrit(dice):
    finalDice = 0
    diceSection = re.split(r'\s\+', dice)
    for di in diceSection:
        if "d" in di:
            maxDie = int(re.findall(r'd\d+', di)[0][1:])
            print("MaxDie")
            print(maxDie)
            allDice = re.findall(r'[\d*]+,|[\d*]+\)', di)
            print("AllDice")
            print(allDice)
            newDice = [0] * len(allDice)
            count = 0
            for d in allDice:
                dNew = int(re.findall(r'\d+', d)[0])
                newDice[count] = dNew
                count += 1
            sortDice = sorted(newDice)
            for i in range(int(len(newDice)/2)):
                sortDice[i] = maxDie
            print("sortDice")
            print(sortDice)
            if "-" in di:
                finalDice -= sum(sortDice)
            else:
                finalDice += sum(sortDice)
        elif "*" not in di and "/" not in di and di != "":
            finalDice += int(di)
    return finalDice

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event    
async def on_message(message):
    if message.author == client.user:
        return
    #print(str(message.author))

    if str(message.author) == 'Avrae#6944':
        msg = message.embeds[0]
        #Initialize message
        response = ""
        if "attacks" in msg.title or "casts" in msg.title or "uses" in msg.title:
            mFields = msg.fields
            for field in mFields:
                if "CRIT!" in field.value and field.name != "Effect":
                    roll = field.value
                    critIndex = roll.find("CRIT!")
                    #Find calculation for crit
                    diceIndex = roll.find(":", critIndex)
                    calc = roll[diceIndex + 2:].split("=")[0]
                    calcList = re.split(r'\]\)*|\[', calc) #Split into smaller pieces
                    print(calcList)
                    # Pass to assign method
                    # Look ahead for mod
                    i = 0
                    while (i + 1) < len(calcList):
                        dice = calcList[i]
                        kind = calcList[i + 1]
                        kindCrit = damCrit(dice)
                        if (i + 2) < len(calcList):
                            nextDice = calcList[i + 2]
                            if " * " in nextDice or "/" in nextDice:
                                mult = re.findall(r'^...\d+', nextDice)[0]
                                multVal = int(re.findall(r'\d+', mult)[0])
                                if "*" in mult:
                                    kindCrit *= multVal
                                else:
                                    kindCrit /= multVal
                        i += 2
                        response += "**" + kind + ": **" + str(kindCrit) + "\n"
                    await message.channel.send(response)

client.run(TOKEN)
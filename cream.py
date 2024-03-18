#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authored-by: Khalil Stroman and Alex Dalton

import os
import re
import dotenv as env
import random
from discord.ext import commands
# Set API_KEY from .env file
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("TOKEN")


bot = commands.Bot(commands_prefix = '!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return  
      
    elif "cookie" in message.content.lower():
        if str(message.author) == "alxdolphin":
            await message.channel.send("Are you talking to me, sir? Your wish is my command!")
        else:
            await message.channel.send("Are you talking to me? I'm glad to assist!")

@bot.command(name = 'flip', help = 'Flips a coin for Heads or Tails')
async def coin_flip(ctx):
    options = ['Heads!', 'Tails!']

    response = random.choice(options)
    await ctx.send(response)

bot.run(API_KEY)


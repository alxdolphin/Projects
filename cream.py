#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authored-by: Khalil Stroman and Alex Dalton
import os
import re
import dotenv as env
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set API_KEY from .env file
load_dotenv()
API_KEY = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

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

    await bot.process_commands(message)
    
@bot.command()
async def flip(ctx):
    options = ['Heads!', 'Tails!']
    response = random.choice(options)
    await ctx.send(response)

bot.run(API_KEY)


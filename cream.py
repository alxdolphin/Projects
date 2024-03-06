#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authored-by: Khalil Stroman and Alex Dalton

import os
import re
import dotenv as env

import discord

# Set API_KEY from .env file
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  
    if message.content.startswith("Cookie") or message.content.startswith("cookie"):
        await message.channel.send("Are you talking to me? I'm glad to assist!")

client.run(API_KEY)




#!/usr/bin/env 
# -*- coding: utf-8 -*-
# Authored-by: Khalil Stroman and Alex Dalton
import os
import re
import dotenv as env
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl
from discord import FFmpegPCMAudio
from discord.utils import get
from collections import deque
import asyncio

# Set API_KEY from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

#Music Queue
servers = {}

def addSong(voiceChannel, url):
    if voiceChannel in servers:
        servers[voiceChannel].append(url)
    else:
        servers[voiceChannel] = deque()
        servers[voiceChannel].append(url)

async def play_next(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel in servers and len(servers[voice_channel]) > 0:
        url = servers[voice_channel].popleft()
        await play(ctx, url)
    


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
    
@bot.command()    
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel and voice_channel.is_connected():
        await voice_channel.move_to(channel)
    else:
        voice_channel = await channel.connect()

@bot.command()
async def leave(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel and voice_channel.is_connected():
        await voice_channel.disconnect()

@bot.command()
async def play(ctx, *args):
    url = ' '.join(args)
    channel = ctx.message.author.voice.channel
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel and voice_channel.is_connected():
        if not voice_channel.is_playing():
            with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                if "youtube.com" in url:
                    info = ydl.extract_info(url, download=False)
                    title = info['title']
                    url2 = info['formats'][0]['url']
                else:
                    query = url
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                    title = info['title']
                    url2 = info['formats'][0]['url']
                voice_channel.play(FFmpegPCMAudio(url2), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
                await ctx.send(f'Playing...{title}')
        else:
            with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                if "youtube.com" in url:
                    info = ydl.extract_info(url, download=False)
                    title = info['title']
                    
                else:
                    info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
                    title = info['title']
                addSong(voice_channel, title)
                await ctx.send(f'Added to queue...{title}')

    else:
        voice_channel = await channel.connect()
        await play(ctx, url)
    

@bot.command()    
async def skip(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel and voice_channel.is_connected():
        voice_channel.stop()
        if voice_channel in servers and len(servers[voice_channel]) > 0:
            url = servers[voice_channel].popleft()
            await ctx.send('Skipping...')
            await play(ctx, url)
        else:
            await ctx.send('Skipping...')

@bot.command()
async def queue(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    curr = list(servers[voice_channel])
    num = 1
    for song in curr:
        await ctx.send(f"{num}. {song}")
        num += 1
    
@bot.command()
async def remove(ctx, num):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    curr = list(servers[voice_channel])
    if int(num) > len(curr):
        await ctx.send("Invalid number")
    else:
        song = curr.pop(int(num)-1)
        servers[voice_channel] = deque(curr)
        await ctx.send(f"Removed {song} from queue")
bot.run(API_KEY)
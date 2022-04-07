import asyncio
import functools
import itertools
import math
import random
import os
import ffmpeg


import youtube_dl
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from async_timeout import timeout


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@client.command()
async def play(ctx, url):
    if ctx.author.voice:
        filename = await YTDLSource.from_url(url, loop=client.loop)
        await ctx.guild.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    else:
        await ctx.send("Join voice channel first")


@client.command()
async def stop(ctx):
    if ctx.author.voice:
        await ctx.guild.voice_client.stop()
    else:
        await ctx.send("Join voice channel first")


@client.command()
async def pause(ctx):
    if ctx.author.voice:
        await ctx.guild.voice_client.pause()
    else:
        await ctx.send("Join voice channel first")


@client.command()
async def resume(ctx):
    if ctx.author.voice:
        await ctx.guild.voice_client.resume()
    else:
        await ctx.send("Join voice channel first")


@client.event
async def on_ready():
    print('We have logged in')


@client.command()
async def hello(ctx):
    await ctx.send("Hello")


@client.command()
async def ass(ctx):
    await ctx.send("https://c.tenor.com/bnSxrkjxW_MAAAAC/ass-we.gif")


@client.command()
async def billy(ctx):
    await ctx.send("https://tenor.com/view/billy-herrington-dotman2-gif-18657898")


@client.command()
async def drive(ctx):
    await ctx.send("https://tenor.com/view/drive-drama-ryan-gosling-crying-sad-gif-3354510")


@client.command()
async def dm(ctx):
    await ctx.send("https://thumbs.gfycat.com/SaneIndolentAmericansaddlebred-max-1mb.gif")


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Join voice channel first")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel")


client.run('YOUR TOKEN HERE')

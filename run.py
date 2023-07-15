from dotenv import load_dotenv
import yt_dlp
import os
import discord
from discord.ext import commands
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
test_url2 = "https://youtu.be/pf6zXMe5TfY"

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def ydl_hook(d):
    if d['status'] == 'finished':
        print("Download finished...")

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    #'outtmpl' : {'default': ''}
    'logger': MyLogger(),
    'progress_hooks': [ydl_hook],
    "postprocessors": [{"key": "FFmpegExtractAudio"}]
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

song_queue = []

@bot.event
async def on_ready():
    print("megabot is ready")
    guilds = bot.guilds
    print(guilds)

@bot.event
async def on_guild_join(guild):
    print(f"joined {guild.name}")

@bot.command()
async def play(ctx,song):
    #check if caller in vc, if not return, else join and play song
    #None if not connected to channel
    author_voice = ctx.author.voice
    if author_voice is None:
        await ctx.send("Connect to a voice channel first")
        return
    
    #ctx.voice_client is none if bot is not connected.
    bot_voice = ctx.voice_client
    if bot_voice is None:
        bot_voice = await author_voice.channel.connect()
   
    #bot is connected to voice channel
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ydl.extract_info(url=song, download=False))
    url2 = data['url'] #data['url'] works, data['formats'][0]['url'] doesnt work

    if not bot_voice.is_playing():
        bot_voice.play(discord.FFmpegPCMAudio(source=url2), after=lambda e: play_next(ctx))
    else:
        song_queue.append(url2)
        await ctx.send("Song queued")
    print("play command finished")

def play_next(ctx):
    voice_channel = ctx.voice_client
    #check if already playing audio
    if voice_channel.is_playing():
        voice_channel.stop()
    if len(song_queue) > 0:
        url = song_queue[0]
        del song_queue[0]
        voice_channel.play(discord.FFmpegPCMAudio(source=url), after=lambda e: play_next(ctx))

@bot.command()
async def skip(ctx):
    voice_channel = ctx.voice_client
    if len(song_queue) == 0 and voice_channel.is_playing():
        voice_channel.stop()
        await ctx.send("Skipping song, no more songs in queue")
        return
    play_next(ctx)

@bot.command()
async def stop(ctx):
    # Check if the bot is connected to a voice channel
   # global voice_channel

    if ctx.voice_client is None:
        await ctx.send("megabot is not connected to a voice channel.")
        return
    
    #voice_channel = None
    # Stop playing and disconnect
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()

if __name__ == '__main__':
    print("bot starting")
    bot.run(DISCORD_TOKEN)

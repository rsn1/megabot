from dotenv import load_dotenv
import youtube_dl
import os
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}


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
    #check if in vc, if not, join and play song

    #None if not connected to channel
    voice = ctx.author.voice
    if voice is None:
        await ctx.send("Connect to a voice channel first")
        return
    
    await voice.channel.connect()



    #await ctx.send(song)

@bot.command()
async def skip(ctx):
    pass


#await - do not continue until this is complete
if __name__ == '__main__':
    print("bot starting")
    bot.run(DISCORD_TOKEN)
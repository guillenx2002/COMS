import discord
import os
from discord.ext import commands
from mcrcon import MCRcon
from dotenv import load_dotenv
import google.generativeai as genai

# Load settings from .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
RCON_IP = os.getenv('RCON_IP')
RCON_PORT = int(os.getenv('RCON_PORT'))
RCON_PASS = os.getenv('RCON_PASS')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'DRAVIK Assistant is online as {bot.user}')

@bot.command()
@commands.is_owner() # Only you can run this
async def rcon(ctx, *, command):
    try:
        with MCRcon(RCON_IP, RCON_PASS, port=RCON_PORT) as mcr:
            response = mcr.command(command)
           # Use this exact line to ensure the quotes are closed properly
        await ctx.send(f"Server response: ```{response}```")
    except Exception as e:
        await ctx.send(f"Error connecting to server: {e}")

bot.run(TOKEN)
import discord
import os
from discord.ext import commands
from mcrcon import MCRcon
from dotenv import load_dotenv

# 1. Load your settings
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
RCON_IP = os.getenv('RCON_IP')
RCON_PORT = int(os.getenv('RCON_PORT'))
RCON_PASS = os.getenv('RCON_PASS')

# 2. DEFINE THE BOT FIRST
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 3. EVENTS AND LOGIC
@bot.event
async def on_ready():
    print(f'DRAVIK Assistant is online as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Your authorized ID
    MY_ID = 1330858852526067732

    # Check for mention AND permission
    if bot.user.mentioned_in(message):
        if message.author.id == MY_ID:
            # Extract the command (remove the mention)
            content = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
            
            if content:
                try:
                    with MCRcon(RCON_IP, RCON_PASS, port=RCON_PORT) as mcr:
                        response = mcr.command(content)
                    await message.channel.send(f"Result: ```{response}```")
                except Exception as e:
                    await message.channel.send(f"Error: {e}")
        else:
            await message.channel.send("Access Denied. Only the administrator can control me.")

    # Allow other commands (like !rcon) to still work
    await bot.process_commands(message)

# 4. Run the bot
bot.run(TOKEN)

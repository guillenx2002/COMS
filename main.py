@bot.event
async def on_message(message):
    # 1. Ignore bot's own messages
    if message.author == bot.user:
        return

    # 2. Your ID
    MY_ID = 1330858852526067732

    # 3. Check for mention AND permission
    if bot.user.mentioned_in(message):
        if message.author.id == MY_ID:
            # Extract the command (everything after the mention)
            content = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
            
            if content:
                # Send to RCON
                try:
                    with MCRcon(RCON_IP, RCON_PASS, port=RCON_PORT) as mcr:
                        response = mcr.command(content)
                    await message.channel.send(f"Result: ```{response}```")
                except Exception as e:
                    await message.channel.send(f"Error: {e}")
        else:
            await message.channel.send("Access Denied.")

    # Allow other commands (like !rcon) to still work
    await bot.process_commands(message)
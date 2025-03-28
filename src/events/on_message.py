from config import *

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}') # print message
    await bot.process_commands(message)
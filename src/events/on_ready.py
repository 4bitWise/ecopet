from config import *

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
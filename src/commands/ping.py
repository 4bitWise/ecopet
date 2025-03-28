import discord
from config import bot

@bot.command(help="Ping to verify if the bot is currently online")
async def ping(ctx):
    await ctx.send('pong')
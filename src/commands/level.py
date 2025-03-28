import discord
from discord.ext import commands
from config import bot
import json
import random
from .action import load_data, max_level_message

@bot.command(help='Display your stats')
async def stats(ctx):
    user_id = str(ctx.author.id)
    data = load_data()
    
    user_data = data.get(user_id, {
        'xp': 0,
        'level': 1,
        'actions_count': 0,
        'name': f"{ctx.author.name}#{ctx.author.discriminator}"
    })
    
    stats_msg = (
        f"**{ctx.author.display_name}'s EcoPet Stats**\n"
        f"• Level: **{user_data['level']}**\n"
        f"• XP: **{user_data['xp']}**\n"
        f"• Actions: **{user_data['actions_count']}**\n"
    )
    
    if user_data['level'] == 5:
        stats_msg += f"\n**{max_level_message}**"
    
    await ctx.send(stats_msg)

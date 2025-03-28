import discord
from discord.ext import commands
from config import bot
import json
import random

levels = [
    {'level': 1, 'required_xp': 0, 'message': None},
    {'level': 2, 'required_xp': 10, 'message': "Your EcoPet is growing! Keep up the great work!"},
    {'level': 3, 'required_xp': 25, 'message': "Your EcoPet is getting stronger! The planet thanks you!"},
    {'level': 4, 'required_xp': 50, 'message': "Your EcoPet is thriving! You're making a real impact!"},
    {'level': 5, 'required_xp': 100, 'message': "Your EcoPet is legendary! You're a true eco-warrior!"},
]

max_level_message = "You've reached the ultimate eco-tier! Inspire others to follow your lead!"
level_messages = {level['level']: level['message'] for level in levels if level['message']}

# Data storage functions
DATA_FILE = 'ecopet_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Level calculation
def get_level(xp):
    for level in reversed(levels):
        if xp >= level['required_xp']:
            return level['level']
    return 1

@bot.command(help='Log an eco-friendly action and earn XP: valid actions include "plant", "planter", "covoiturage", "transport en commun", "recycler"')
async def action(ctx, *, action: str):
    user_id = str(ctx.author.id)
    data = load_data()
    
    if action in ["plant", "planter", "covoiturage", "transport en commun", "recycler"]:
        user_data = data.get(user_id, {
            'xp': 0,
            'level': 1,
            'actions_count': 0,
            'name': f"{ctx.author.name}#{ctx.author.discriminator}"
        })
        
        user_data['name'] = f"{ctx.author.name}#{ctx.author.discriminator}"
        user_data['actions_count'] += 1
        xp_earned = random.randint(3, 7)
        user_data['xp'] += xp_earned
        
        new_level = get_level(user_data['xp'])
        current_level = user_data['level']
        
        if new_level > current_level:
            for lvl in range(current_level + 1, new_level + 1):
                if msg := level_messages.get(lvl):
                    await ctx.send(f"{ctx.author.mention}, {msg}")
            user_data['level'] = new_level
        
        data[user_id] = user_data
        save_data(data)
        await ctx.send(f"{ctx.author.mention}, Action logged: **{action}**! +{xp_earned} XP!")
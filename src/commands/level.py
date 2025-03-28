import discord
from discord.ext import commands
from config import bot, openapikey
import json
import random
from .action import load_data, max_level_message
import openai

OpenAI_API_Key = openapikey
openai.api_key = OpenAI_API_Key

prompt_by_level = {
    0: "A cute Ghibli-style tree at level 0, designed as the first stage of its evolution. The tree is small, chubby, and whimsical, with a short, stubby trunk and no leaves. It has an expressive and friendly face subtly integrated into its bark, giving it a magical personality. The design is soft and warm, evoking a fantasy feel. No background, no text.",
    1: "A cute Ghibli-style tree at level 1, evolving from its level 0 form. The tree is slightly taller and stronger, with small budding leaves starting to grow at the tips of its branches. The trunk is a bit thicker, still with an expressive and friendly face integrated into the bark. Its magical and whimsical charm remains. No background, no text.",
    2: "A cute Ghibli-style tree at level 2, continuing its evolution. Now the tree has more visible branches with small clusters of fresh green leaves. The trunk is stronger and slightly more textured, while its friendly face maintains a warm and lively expression. The tree starts to feel more alive and connected to nature. No background, no text.",
    3: "A cute Ghibli-style tree at level 3, reaching a more mature stage of its evolution. The tree now has a full canopy of lush green leaves, with small magical sparkles around it. Its trunk is thicker, with gentle curves and knots that enhance its personality. The face remains expressive, showing wisdom and kindness. No background, no text.",
    4: "A cute Ghibli-style tree at level 4, nearly reaching its final form. The tree has grown tall and strong, with a dense canopy of leaves that provide a protective and comforting aura. The trunk is wide with visible roots, and its face exudes warmth and wisdom. Small magical lights or tiny creatures may appear near it, emphasizing its mystical nature. No background, no text.",
    5: "A majestic Ghibli-style tree at level 5, fully evolved into its grand form. The tree is now large and magnificent, with a thick, ancient-looking trunk and vibrant, full foliage. Its face remains expressive, radiating wisdom and kindness. Tiny glowing particles or small magical creatures surround it, giving it a legendary presence. The design is warm, magical, and awe-inspiring. No background, no text.",
}

def generate_pet_image(level):
    prompt = prompt_by_level[level]

    img_params = {
        "model": "dall-e-3",
        "n": 1,
        "size": "1792x1024",
        "prompt": prompt,
    }

    response = openai.images.generate(**img_params)
    img_url = response.data[0].url
    return img_url

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
    
    embed = discord.Embed(description=stats_msg, color=discord.Color.green())
    try:
        # Get level-appropriate image
        pet_image_url = await ctx.bot.loop.run_in_executor(
            None,  # Uses default executor
            generate_pet_image,
            user_data['level']
        )
        embed.set_image(url=pet_image_url)
    except Exception as e:
        print(f"Error generating pet image: {e}")
        embed.set_footer(text="Couldn't generate pet image this time 🌱")

    await ctx.send(embed=embed)

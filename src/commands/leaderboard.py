from .action import load_data, get_level
from config import bot

@bot.command(help='Show top eco-friendly users')
async def leaderboard(ctx):
    data = load_data()
    sorted_users = sorted(
        [(ud['xp'], ud['name'], ud['actions_count']) for ud in data.values()],
        key=lambda x: (-x[0], -x[2], x[1])
    )[:10]
    
    leaderboard_msg = "**🌿 Top Eco Warriors 🌿**\n"
    for i, (xp, name, actions) in enumerate(sorted_users, 1):
        leaderboard_msg += (
            f"{i}. {name} - "
            f"Level {get_level(xp)} | "
            f"XP: {xp} | "
            f"Actions: {actions}\n"
        )
    
    await ctx.send(leaderboard_msg)
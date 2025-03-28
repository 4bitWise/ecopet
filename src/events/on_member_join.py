from config import *

@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    # system_channel utilise le channel defini pour recevoir des messages systemes.
    # Si il n'est pas defini, on doit envoyer le message dans un channel random
    if guild.system_channel is not None:
        message = f"Welcome {member.mention} to {guild.name} !"
        await guild.system_channel.send(message)
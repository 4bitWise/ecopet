#!/usr/bin/python3.12

import os
import discord, asyncio
from dotenv import load_dotenv
from discord.ext import commands
from help.help import Help
from help.helpCog import HelpCog, setup

# loading environment config
load_dotenv('.conf')

# getting discord bot token
token = os.getenv("TOKEN")
openapikey = os.getenv("OpenAI_API_Key")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.help_command = Help()
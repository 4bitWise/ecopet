#!/usr/bin/python3.12

import os
from config import *
from commands import ping
from events import on_member_join
from events import on_message
from events import on_ready

# running bot
bot.run(token)
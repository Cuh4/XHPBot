# // ---------------------------------------------------------------------
# // ------- [Embeds] Bot
# // ---------------------------------------------------------------------

"""
An embed giving info on the provided bot.
Repo: https://github.com/cuhHub/ArcheanBot

---

Copyright (C) 2024 Cuh4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# ---- // Imports
import discord
import psutil
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

from datetime import datetime, timedelta

# ---- // Main
class Bot(discord.Embed):
    """
    An embed displaying information on the provided bot.
    """
    
    def __init__(self, bot: "Bot"):
        """
        An embed displaying information on the provided bot.

        Args:
            bot (Bot): The bot.
        """
        
        super().__init__()
        
        # Get stats
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 ** 2)
        cpu_usage_percent = process.cpu_percent()
        uptime_formatted = timedelta(seconds = (datetime.now() - datetime.fromtimestamp(bot.started_at)).seconds) # creating timedelta object when subtraction creates one anyway is purely for formatting https://stackoverflow.com/a/13409830
        
        # Create embed
        self.title = "Bot Information"
        self.color = discord.Color.from_rgb(175, 255, 175)
        self.description = "\n".join([f"`/{command.name}`: {command.description}" for command in bot.tree.get_commands()])
        
        self.add_field(name = "Memory Usage", value = f"{memory_usage:.1f}MB", inline = True)
        self.add_field(name = "CPU Usage", value = f"{cpu_usage_percent:.1f}%", inline = True)
        self.add_field(name = "Uptime", value = f"{uptime_formatted}", inline = True)
        self.add_field(name = "Source Code", value = f"[**Click Here**]({os.getenv("github_repo_url")})", inline = False)
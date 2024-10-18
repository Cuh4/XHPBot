# // ---------------------------------------------------------------------
# // ------- [Embeds] Bot
# // ---------------------------------------------------------------------

"""
An embed giving info on the provided bot.
Repo: https://github.com/Cuh4/XHPBot

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
def embed(bot: "Bot") -> discord.Embed:
    """
    Returns an embed giving info on the provided bot.

    Args:
        bot (Bot): The bot.

    Returns:
        Embed: The success embed.
    """
    
    # Embed
    embed = discord.Embed(
        title = "Bot Information",
        color = discord.Color.from_rgb(175, 255, 175)
    )
    
    # Stats
    process = psutil.Process(os.getpid())
    memoryUsage = process.memory_info().rss / (1024 ** 2)
    CPUUsagePercent = process.cpu_percent()
    uptimeFormatted = timedelta(seconds = (datetime.now() - datetime.fromtimestamp(bot.StartedAt)).seconds) # creating timedelta object when subtraction creates one anyway is purely for formatting https://stackoverflow.com/a/13409830
    
    # Commands
    embed.description = "\n".join([f"`/{command.name}`: {command.description}" for command in bot.tree.get_commands()])

    # Statistics/Links
    embed.add_field(name = "Memory Usage", value = f"{memoryUsage:.1f}MB", inline = True)
    embed.add_field(name = "CPU Usage", value = f"{CPUUsagePercent:.1f}%", inline = True)
    embed.add_field(name = "Uptime", value = f"{uptimeFormatted}", inline = True)
    embed.add_field(name = "Source Code", value = f"[**Click Here**]({os.getenv("github_repo_url")})", inline = False)
    
    return embed
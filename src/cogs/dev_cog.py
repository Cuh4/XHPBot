# // ---------------------------------------------------------------------
# // ------- [Cogs] Dev Cog
# // ---------------------------------------------------------------------

"""
A cog for developer commands, etc.
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
from discord import app_commands
import subprocess
import sys

from cogs.base_cog import BaseCog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import embeds
import checks

# ---- // Main
class DevCog(BaseCog):
    """
    A cog for providing commands related to bot info.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `InfoCog` class objects.
        """        
        
        super().__init__(bot)
        
    # ---- // Methods
    def restart_bot(self, update: bool = False):
        """
        Restarts the bot, updating beforehand if requested.

        Args:
            update (bool, optional): Whether or not to update the bot via `git pull`. Defaults to False.
        """
       
        if update:
            subprocess.call("git pull")
           
        subprocess.Popen([sys.executable, *sys.argv])
        exit(0)
            
    # ---- // Commands
    @app_commands.command(name = "restart")
    @app_commands.default_permissions(administrator = True)
    async def RestartCommand(self, interaction: discord.Interaction, update: bool = False):
        """
        Restarts the bot.

        Args:
            interaction (discord.Interaction): The context of the command.
            update (bool, optional): Whether or not to update the bot via `git pull`. Defaults to False.
        """
        
        await checks.bot.ready(interaction)
        await interaction.response.send_message(ephemeral = True, embed = embeds.Success("Restarting..."))
        
        self.restart_bot(update = update)
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(DevCog(bot))
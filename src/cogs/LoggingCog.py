# // ---------------------------------------------------------------------
# // ------- [Cogs] Logging Cog
# // ---------------------------------------------------------------------

"""
A cog for logging common bot events.
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
from discord.ext import commands

from cogs.BaseCog import BaseCog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

from libs import print

# ---- // Main
class LoggingCog(BaseCog):
    """
    A cog for logging common bot events.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `LoggingCog` class objects.
        """        
        
        super().__init__(bot)
        
    # ---- // Events
    @commands.Cog.listener("on_interaction")
    async def OnInteractionListener(self, interaction: discord.Interaction):
        """
        Called when an interaction is received.

        Args:
            interaction (discord.Interaction): The interaction received.
        """
        
        print.info(self.qualified_name, f"Received an interaction of type '{interaction.type}' from {interaction.user}")
    
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(LoggingCog(bot))
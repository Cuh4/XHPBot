# // ---------------------------------------------------------------------
# // ------- [Cogs] Base Cog
# // ---------------------------------------------------------------------

"""
A base cog class to inherit from.
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
import threading

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

from abc import abstractmethod

# ---- // Main
class BaseCog(commands.Cog):
    """
    A base cog class to inherit from.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `BaseCog` class objects.
        """        
        
        self.Bot = bot
        self.Database = self.Bot.Database
        
    async def Start(self):
        """
        Starts this cog.
        """
        
        threading.Thread(target = self.CogStart).start()
        await self.CogStartAsync()
        
    @commands.Cog.listener("on_ready")
    async def OnReadyListener(self):
        """
        Called when the bot is ready.
        """
        
        await self.Start()
        
    @abstractmethod
    def CogStart(self):
        """
        Called when the cog is started (non-async).
        """
        
    @abstractmethod
    async def CogStartAsync(self):
        """
        Called when the cog is started (async).
        """        
        
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    pass
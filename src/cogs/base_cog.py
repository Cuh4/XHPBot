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
        
        self.bot = bot
        self.json_db = self.bot.json_database
        self.sql_db = self.bot.sql_database
        
    async def start(self):
        """
        Starts this cog.
        """
        
        threading.Thread(target = self.cog_start).start()
        await self.cog_start_async()
        
    @commands.Cog.listener("on_ready")
    async def on_ready_listener(self):
        """
        Called when the bot is ready.
        """
        
        await self.start()
        
    @abstractmethod
    def cog_start(self):
        """
        Called when the cog is started (non-async).
        """

        pass
        
    @abstractmethod
    async def cog_start_async(self):
        """
        Called when the cog is started (async).
        """
        
        pass
        
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """
    
    pass
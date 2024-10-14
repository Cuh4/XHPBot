# // ---------------------------------------------------------------------
# // ------- Bot
# // ---------------------------------------------------------------------

"""
A custom class descending from discord.ext.commands.Bot.
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

from threading import Thread

from libs.db import Database

from libs.archean import (
    Archean
)

from services import (
    StatusService
)

# ---- // Main
class Bot(commands.Bot):
    """
    A custom class descending from discord.ext.commands.Bot.
    """    
    
    def __init__(self, database: Database, archean: Archean):
        """
        Initializes the bot.

        Args:
            database (Database): The database to use.
            archean (Archean): The Archean API wrapper to use.
        """        
        
        super().__init__(
            command_prefix = "!",
            intents = discord.Intents(messages = True, guilds = True)
        )
        
        self.Database = database
        self.Archean = archean
        
        # Services
        self.StatusService = StatusService()
        
        self.Services = [
            self.StatusService
        ]

    async def on_ready(self):
        """
        Called when the bot is ready.
        """        
        
        print(f"[:)] Bot is online @ {self.user.name} ({self.user.id})")
        
        for service in self.Services:
            await service.Start(self)
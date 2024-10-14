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

import os
import time

from jsonstore import JsonStore
from libs import print

# ---- // Main
class Bot(commands.AutoShardedBot):
    """
    A custom class descending from discord.ext.commands.Bot.
    """    
    
    def __init__(self, database: JsonStore):
        """
        Initializes the bot.

        Args:
            database (Database): The database to use.
        """        
        
        super().__init__(
            intents = discord.Intents.all()
        )
        
        self.Database = database
        self.StartedAt = 0
        self.Ready = False

    async def LoadCogs(self):
        """
        Loads all cogs in the `cogs` directory.
        """
        
        for cog in os.listdir("cogs"):
            if cog.endswith(".py"):
                await self.load_extension(f"cogs.{cog[:-3]}")
                print.success("Cogs", f"Loaded `{cog}`.")

    async def setup_hook(self):
        """
        Called before websocket connection, but after client login.
        Used to setup cogs, etc.
        """        
        
        self.StartedAt = time.time()
        await self.LoadCogs()

    async def on_ready(self):
        """
        Called when the bot is ready.
        """        
        
        print.success("Bot", f"Bot is online @ {self.user.name} ({self.user.id})")
        self.Ready = True
        await self.tree.sync()
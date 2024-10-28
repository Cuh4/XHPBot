# // ---------------------------------------------------------------------
# // ------- [Cogs] Info Cog
# // ---------------------------------------------------------------------

"""
A cog for providing commands related to bot info.
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
from discord.ext import commands

from cogs.base_cog import BaseCog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import embeds
import checks

# ---- // Main
class InfoCog(BaseCog):
    """
    A cog for providing commands related to bot info.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `InfoCog` class objects.
        """        
        
        super().__init__(bot)
        
    # ---- // Events
    @commands.Cog.listener("on_message")
    async def on_message_listener(self, message: discord.Message):
        """
        Called when a message is received.

        Args:
            message (discord.Message): The message received.
        """
        
        if not self.bot.user in message.mentions:
            return
        
        if message.author.bot:
            return
        
        # Show info when pinged (or show info to the user that the message author replied to)
        if message.reference is not None:
            message = await message.channel.fetch_message(message.reference.message_id)
        
        await message.reply(embed = embeds.Bot(self.bot), mention_author = True)
            
    # ---- // Commands
    @app_commands.command(name = "info")
    async def InfoCommand(self, interaction: discord.Interaction):
        """
        Provides information about the bot.

        Args:
            interaction (discord.Interaction): The context of the command.
        """
        
        await checks.bot.ready(interaction)
        await interaction.response.send_message(ephemeral = True, embed = embeds.Bot(self.bot))
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(InfoCog(bot))
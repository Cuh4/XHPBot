# // ---------------------------------------------------------------------
# // ------- [Cogs] Status Cog
# // ---------------------------------------------------------------------

"""
A cog for showing the status of the XHP server, as well as providing commands.
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
from discord.ext.tasks import loop
from discord import app_commands

from cogs.BaseCog import BaseCog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import libs.env as env
from libs import print

from libs.archean import (
    Archean,
    Server
)

import embeds
import checks

# ---- // Main
class StatusCog(BaseCog):
    """
    A cog for showing the status of the XHP server.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `StatusCog` class objects.
        """        
        
        super().__init__(bot)

        self.Archean = Archean()
        self.ServerIP = env.GetServerIP()[0]
        self.ServerPort = env.GetServerIP()[1]
        
        self.StatusLoop = loop(seconds = env.GetStatusRefreshRate())(self.UpdateStatus)

    # ---- // Callbacks
    async def CogStartAsync(self):
        # Get channel for server status message
        try:
            self.StatusChannel = self.Bot.get_channel(env.GetStatusChannel()) or await self.Bot.fetch_channel(env.GetStatusChannel())
            
            if self.StatusChannel is None: # get_channel() returns None
                raise discord.NotFound
        except discord.NotFound:
            print.error(self.qualified_name, "Status channel doesn't exist. Please create one and update .env!")
            exit(0)

        # Get message if already sent, otherwise send a new one
        try:
            self.StatusMessage = await self.StatusChannel.fetch_message(self.GetSavedStatusMessageID() or 0)
        except discord.NotFound:
            print.info(self.qualified_name, "Status message doesn't exist. Sending a new one!")
            self.StatusMessage = await self.StatusChannel.send(embed = embeds.Info("Setting up..."))
            self.SaveStatusMessageID()
            
        # Start loop
        self.StatusLoop.start()
        
    # ---- // Methods
    def GetSavedStatusMessageID(self) -> int|None:
        """
        Returns the message ID of the server status message if any.

        Returns:
            int|None: The message ID, or none if not saved.
        """        
        
        try:
            return self.Database.status_message_id
        except AttributeError:
            return None
    
    def SaveStatusMessageID(self):
        """
        Saves the message ID of the server status message.
        """        
        
        self.Database.status_message_id = self.StatusMessage.id
        
    async def FetchServerInformation(self) -> Server|None:
        """
        Returns the target server.

        Returns:
            Server|None: The server to show server status for.
        """        
        
        return await self.Archean.GetServerByIP(self.ServerIP, self.ServerPort)
    
    async def UpdateStatus(self):
        """
        Updates server status.
        """        
        
        # Get server information
        try:
            server = await self.FetchServerInformation()
        except Exception as error:
            print.error(self.qualified_name, f"Failed to fetch server information: {error}")
            server = None
        
        # Edit message
        try:
            await self.StatusMessage.edit(embed = embeds.Server(server))
        except discord.HTTPException as error:
            print.error(self.qualified_name, f"Failed to update server status message: {error}")
            
    # ---- // Commands
    @app_commands.command(name = "status")
    @app_commands.check(checks.bot.Ready)
    async def StatusCommand(self, interaction: discord.Interaction):
        """
        Shows the status of the server.

        Args:
            interaction (discord.Interaction): The context of the command.
        """            
        
        server = await self.FetchServerInformation()
        await interaction.response.send_message(ephemeral = True, embed = embeds.CompactServer(server))
        
    @app_commands.command(name = "online")
    @app_commands.check(checks.bot.Ready)
    async def OnlineCommand(self, interaction: discord.Interaction):
        """
        Shows if the server is online or not.

        Args:
            interaction (discord.Interaction): The context of the command.
        """             
        
        server = await self.FetchServerInformation()
        
        if server is not None:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Info(f"🟢 | The server is online."))
        else:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Error("🔴 | The server is offline."))
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(StatusCog(bot))
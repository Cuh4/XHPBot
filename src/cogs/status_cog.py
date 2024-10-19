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
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

from cogs.base_cog import BaseCog

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

        self.archean = Archean()
        self.server_ip = os.getenv("server_ip").split(":")[0]
        self.server_port = int(os.getenv("server_ip").split(":")[1])
        
        self.status_loop = loop(seconds = float(os.getenv("status_update_interval")))(self.update_status)

    # ---- // Callbacks
    async def cog_start_async(self):
        # Get channel for server status message
        try:
            self.status_channel = self.bot.get_channel(os.getenv("status_channel")) or await self.bot.fetch_channel(os.getenv("status_channel"))
            
            if self.status_channel is None: # get_channel() returns None
                raise discord.NotFound
        except discord.NotFound: # fetch_channel() raises an exception
            print.error(self.qualified_name, "Status channel doesn't exist. Please create one and update .env!")
            exit(0)

        # Get message if already sent, otherwise send a new one
        try:
            self.status_message = await self.status_channel.fetch_message(self.json_db.get("status_message_id") or 0)
        except discord.NotFound:
            print.info(self.qualified_name, "Status message doesn't exist. Sending a new one!")

            self.status_message = await self.status_channel.send(embed = embeds.Info("Setting up..."))
            self.json_db.set("status_message_id", self.status_message.id)
            
        # Start loop
        self.status_loop.start()
        
    # ---- // Methods
    async def fetch_server_information(self) -> Server|None:
        """
        Returns the target server.

        Returns:
            Server|None: The server to show server status for.
        """        
        
        return await self.archean.get_server_by_ip(self.server_ip, self.server_port)
    
    async def update_status(self):
        """
        Updates server status.
        """        
        
        # Get server information
        try:
            server = await self.fetch_server_information()
        except Exception as error:
            print.error(self.qualified_name, f"Failed to fetch server information: {error}")
            server = None
        
        # Edit message
        try:
            await self.status_message.edit(embed = embeds.Server(server))
        except discord.HTTPException as error:
            print.error(self.qualified_name, f"Failed to update server status message: {error}")
            
    # ---- // Commands
    @app_commands.command(name = "status")
    @app_commands.check(checks.bot.ready)
    async def status_command(self, interaction: discord.Interaction):
        """
        Shows the status of the server.

        Args:
            interaction (discord.Interaction): The context of the command.
        """            
        
        server = await self.fetch_server_information()
        await interaction.response.send_message(ephemeral = True, embed = embeds.compact_server(server))
        
    @app_commands.command(name = "online")
    @app_commands.check(checks.bot.ready)
    async def online_command(self, interaction: discord.Interaction):
        """
        Shows if the server is online or not.

        Args:
            interaction (discord.Interaction): The context of the command.
        """             
        
        server = await self.fetch_server_information()
        
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
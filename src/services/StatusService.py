# // ---------------------------------------------------------------------
# // ------- [Services] Status Service
# // ---------------------------------------------------------------------

"""
A service for showing the status of the XHP server.
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

from typing import TYPE_CHECKING

if TYPE_CHECKING: # prevent circular dependency error. we only need this bot impor tfor typechecking anyway
    from bot import Bot

import time

import libs.env as env
import libs.embeds as embeds
import libs.timestamp as timestamp

from libs.archean import (
    Server,
    PasswordProtected
)

from . import BaseService

# ---- // Main
class StatusService(BaseService):
    """
    A service for showing the status of the XHP server.
    """
    
    def __init__(self):
        """
        Initializes `StatusService` class objects.
        """        
        
        super().__init__("StatusService")
        
    async def ServiceStartAsync(self, bot: "Bot"):
        """
        Starts the service.

        Args:
            bot (Bot): The bot to pass to the service.
        """
        
        # Set up attributes
        self.Loop = loop(seconds = env.GetRefreshRate())(self.UpdateStatus)
        self.StatusRefreshRate = env.GetRefreshRate()
        self.ServerIP = env.GetServerIP()[0]
        self.ServerPort = env.GetServerIP()[1]
        
        # Get channel for server status message
        try:
            self.StatusChannel = self.Bot.get_channel(env.GetStatusChannel()) or await self.Bot.fetch_channel(env.GetStatusChannel())
            
            if self.StatusChannel is None: # get_channel() returns None
                raise discord.NotFound
        except discord.NotFound:
            print("[>] Status channel doesn't exist. Please create one and update .env!")
            exit(0)

        # Get message if already sent, otherwise send a new one
        try:
            self.StatusMessage = await self.StatusChannel.fetch_message(self.GetSavedStatusMessageID() or 0)
        except discord.NotFound:
            print("[>] Status message doesn't exist. Sending a new one!")
            self.StatusMessage = await self.StatusChannel.send(embed = embeds.Info("Setting up..."))
            self.SaveStatusMessageID()
        
        # Start loop
        self.Loop.start()
        
    def GetSavedStatusMessageID(self) -> int|None:
        """
        Returns the message ID of the server status message if any.

        Returns:
            int|None: The message ID, or none if not saved.
        """        
        
        return self.Bot.Database.Load().get("status_message_id")
    
    def SaveStatusMessageID(self):
        """
        Saves the message ID of the server status message.
        """        
        
        self.Bot.Database.Save({
            "status_message_id" : self.StatusMessage.id
        })
        
    def FetchServerInformation(self) -> Server|None:
        """
        Returns the target server.

        Returns:
            Server|None: The server to show server status for.
        """        
        
        return self.Bot.Archean.GetServerByIP(self.ServerIP, self.ServerPort)
    
    async def UpdateStatus(self):
        """
        Updates server status.
        """        
        
        # Get server information
        try:
            server = self.FetchServerInformation()
        except Exception as error:
            print(f"[-] Failed to fetch server information: {error}")
            server = None
        
        # For later
        lastUpdated = f"{timestamp.FormatTimestamp(time.time(), "R")}"
        
        # Create embed
        if server is None:
            # Offline message
            embed = discord.Embed(
                title = "Server Status",
                description = f"⛔ | The tracked server is offline.\n-# Last updated: {lastUpdated}",
                color = discord.Color.red()
            )
            
            embed.set_footer(text = f"Open-Source @ {env.GetGitHubRepoURL()}")
        else:
            # Online message
            embed = discord.Embed(
                title = f"☀️ | {server.Name}",

                description = "\n".join([
                    f"**⚙️ | {server.Gamemode} Server • " + ("🔒 | Password Protected" if server.PasswordProtected == PasswordProtected.Protected else "🔓 | No Password") + "**",
                    f"🔗 | " + (f"{server.IP}:{server.Port}" if not env.GetHideIP() else "IP Hidden"),
                    f"👥 | {server.Players}/{server.MaxPlayers} Players",
                    "",
                    f"-# Last Updated: {lastUpdated}"
                ]),
                
                color = env.GetStatusEmbedColor()
            )
            
            embed.set_footer(text = f"Server Version: v{server.Version} | Open-Source @ {env.GetGitHubRepoURL()}")
            embed.set_image(url = env.GetStatusBannerURL())
        
        # Edit message
        try:
            await self.StatusMessage.edit(embed = embed)
        except discord.HTTPException as error:
            print(f"[-] Failed to update server status message: {error}")
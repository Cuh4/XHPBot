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
from discord.ext.tasks import loop

import time

import libs.env as env
import libs.embeds as embeds
import libs.timestamp as timestamp
from libs.db import Database

from libs.archean import (
    Archean,
    Server,
    PasswordProtected
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
        self.StatusRefreshRate = env.GetRefreshRate()
        self.ServerIP = env.GetServerIP()[0]
        self.ServerPort = env.GetServerIP()[1]
        
        self.StatusLoop = loop(seconds = self.StatusRefreshRate)(self.UpdateStatus)

    async def on_ready(self):
        """
        Called when the bot is ready.
        """        
        
        print(f"[:)] Bot is online @ {self.user.name} ({self.user.id})")
        print(f"[>] Server status task has started. Tracking {self.ServerIP}:{self.ServerPort}.")
        
        try:
            self.StatusChannel = self.get_channel(env.GetStatusChannel()) or await self.fetch_channel(env.GetStatusChannel())
            
            if self.StatusChannel is None: # get_channel() returns None
                raise discord.NotFound
        except discord.NotFound:
            print("[>] Status channel doesn't exist. Please create one and update .env!")
            exit(0)

        try:
            self.StatusMessage = await self.StatusChannel.fetch_message(self.GetSavedStatusMessageID() or 0)
        except discord.NotFound:
            print("[>] Status message doesn't exist. Sending a new one!")
            self.StatusMessage = await self.StatusChannel.send(embed = embeds.Info("Setting up..."))
            self.SaveStatusMessageID()
        
        self.StatusLoop.start()
        
    def GetSavedStatusMessageID(self) -> int|None:
        """
        Returns the message ID of the server status message if any.

        Returns:
            int|None: The message ID, or none if not saved.
        """        
        
        return self.Database.Load().get("status_message_id")
    
    def SaveStatusMessageID(self):
        """
        Saves the message ID of the server status message.
        """        
        
        self.Database.Save({
            "status_message_id" : self.StatusMessage.id
        })
        
    def FetchServerInformation(self) -> Server|None:
        """
        Returns the target server.

        Returns:
            Server|None: The server to show server status for.
        """        
        
        return self.Archean.GetServerByIP(self.ServerIP, self.ServerPort)
    
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
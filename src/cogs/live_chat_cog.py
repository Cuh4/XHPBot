# // ---------------------------------------------------------------------
# // ------- [Cogs] Live Chat Cog
# // ---------------------------------------------------------------------

"""
A cog for showing when players join and leave the Archean server.
Repo: https://github.com/cuhHub/ArcheanBot

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
from discord.ext.tasks import loop
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot
    from cogs.status_cog import StatusCog

from cogs.base_cog import BaseCog

from libs import print

from embeds import LiveChat

# ---- // Main
class LiveChatCog(BaseCog):
    """
    A cog for showing when players join and leave the Archean server.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `LiveChatCog` class objects.
        """        
        
        super().__init__(bot)

        self.loop = loop(seconds = float(os.getenv("live_chat_update_interval")))(self.check_player_activity)
        self.previous_player_count = 0

    # ---- // Callbacks
    async def cog_start_async(self):
        """
        Called when the cog starts.
        """

        self.status_cog: "StatusCog" = self.bot.get_cog("StatusCog")
        self.loop.start()
        
        try:
            self.channel = self.bot.get_channel(os.getenv("live_chat_channel_id")) or await self.bot.fetch_channel(os.getenv("live_chat_channel_id"))
            
            if self.channel is None:
                raise discord.HTTPException(".get_channel(...) returned None.")
        except discord.HTTPException as exception:
            print.error(self.qualified_name, f"Failed to fetch live chat channel: {os.getenv("live_chat_channel_id")}. Err: {exception}")
            return
        
    # ---- // Methods
    async def send_player_join_message(self, count: int, max_players: int):
        """
        Sends a message to the live chat channel when a player joins.

        Args:
            count (int): The server player count at the time of the join.
            max_players (int): The server max player count.
        """        
        
        embed = LiveChat(
            title = "Join",
            text = f"A player joined the server. `{count}/{max_players}` players online.",
            color = (0, 255, 0),
            emoji = "📩"
        )
        
        await self.channel.send(embed = embed)
        
    async def send_player_leave_message(self, count: int, max_players: int):
        """
        Sends a message to the live chat channel when a player leaves.

        Args:
            count (int): The server player count at the time of the leave.
            max_players (int): The server max player count.
        """
        
        embed = LiveChat(
            title = "Leave",
            text = f"A player left the server. `{count}/{max_players}` players online.",
            color = (255, 0, 0),
            emoji = "📤"
        )
        
        await self.channel.send(embed = embed)
    
    async def check_player_activity(self):
        """
        Notifies users when the server reaches a player count.
        """        
        
        # Get server info
        try:
            server = await self.status_cog.fetch_server_information()
            
            if server is None:
                raise Exception("Server is None. Could be offline or unreachable.")
        except Exception as error:
            print.error(self.qualified_name, f"Failed to fetch server information: {error}")
            return
        
        if server is None:
            return
        
        # Detect player join/leave
        difference = server.players - self.previous_player_count
        
        if difference > 0:
            for i in range(difference):
                await self.send_player_join_message(self.previous_player_count + i + 1, server.max_players)
        elif difference < 0:
            for i in range(-difference):
                await self.send_player_leave_message(self.previous_player_count - i - 1, server.max_players)
        
        self.previous_player_count = server.players
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(LiveChatCog(bot))
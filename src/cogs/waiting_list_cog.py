# // ---------------------------------------------------------------------
# // ------- [Cogs] Waiting List Cog
# // ---------------------------------------------------------------------

"""
A cog for allowing users to get notified when the server reaches a player count.
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
from libs import timestamp

import checks
import embeds
import models

# ---- // Main
class WaitingListCog(BaseCog):
    """
    A cog for allowing users to get notified when the server reaches a player count.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `WaitingListCog` class objects.
        """        
        
        super().__init__(bot)

        self.notify_loop = loop(seconds = float(os.getenv("waiting_list_update_interval")))(self.notify)

    # ---- // Callbacks
    async def cog_start_async(self):
        self.status_cog: "StatusCog" = self.bot.get_cog("StatusCog")
        self.notify_loop.start()
        
    # ---- // Methods
    async def notify(self):
        """
        Notifies users when the server reaches a player count.
        """        
        
        # Get server info
        try:
            server = await self.status_cog.fetch_server_information()
        except Exception as error:
            print.error(self.qualified_name, f"Failed to fetch server information: {error}")
            return
        
        if server is None:
            return
        
        # Find Waitees for server's player count
        for waitee in models.Waitee.get_waitees_for_player_count(server.players):
            try: # send to dms
                user = await waitee.get_user(self.bot)
                dm_channel = user.dm_channel or await user.create_dm()
                
                await dm_channel.send(embed = embeds.WaiteeReminder(waitee))
            except Exception as error: # failed to send to dms, fallback to channel
                try:
                    user = await waitee.get_user(self.bot)
                    channel = await waitee.get_fallback_channel(self.bot)
                    await channel.send(content = user.mention, embed = embeds.WaiteeReminder(waitee, used_fallback = True))
                except Exception as error:
                    print.error(self.qualified_name, f"Failed to send waitee reminder to {user}: {error}")

            waitee.delete_instance()
            
     # ---- // Commands
    @app_commands.command(name = "wait")
    async def status_command(self, interaction: discord.Interaction, player_count: int):
        """
        Sets you up to be notified when the server reaches a player count.

        Args:
            interaction (discord.Interaction): The context of the command.
            player_count (int): The player count to wait for.
        """
        
        # Checks
        await checks.bot.ready(interaction)            
        
        # Check if the player count is valid
        server = await self.status_cog.fetch_server_information()
        
        if player_count <= 0 or player_count > server.max_players:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Error(f"The player count provided is invalid. Keep it between `1-{server.max_players}`."))
            return
        
        # Check if the player count is already reached
        if player_count == server.players:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Error(f"The player count is already `{player_count}`."))
            return
        
        # Check if the user already has a waitee
        waitee = models.Waitee.get_waitee(interaction.user)
        
        if waitee is not None:    
            # No point in modifying, user is already waiting for the same player count 
            if waitee.wants_player_count == player_count:
                await interaction.response.send_message(ephemeral = True, embed = embeds.Error("You are already waiting for this player count."))
                return
            
            # Update
            waitee.wants_player_count = player_count
            
            try:
                waitee.save()
            except:
                await interaction.response.send_message(ephemeral = True, embed = embeds.Error("Failed to update your reminder."))
                return

            # Notify
            await interaction.response.send_message(ephemeral = True, embed = embeds.Success(f"You will now be notified when the server reaches a player count of `{player_count}`.\nNote that you just modified your existing reminder, so you will not be notified for the old player count.\nUse `/dismiss` to cancel."))
            return
        
        # Create new waitee
        try:
            waitee = models.Waitee.wait_for_count(interaction.user, player_count, interaction.channel)
        except:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Error("Failed to create a reminder."))
            return
            
        await interaction.response.send_message(ephemeral = True, embed = embeds.Success(f"You will now be notified when the server reaches a player count of `{player_count}`.\nUse `/dismiss` to cancel."))
        
    @app_commands.command(name = "dismiss")
    async def dismiss_command(self, interaction: discord.Interaction):
        """
        Removes you from being notified when the server reaches a player count.

        Args:
            interaction (discord.Interaction): The context of the command.
        """            
        
        # Checks
        await checks.bot.ready(interaction)
        
        # Get waitee
        waitee = models.Waitee.get_waitee(interaction.user)
        
        if waitee is None:
            await interaction.response.send_message(ephemeral = True, embed = embeds.Error("You are not currently waiting. Use `/wait` to set up a reminder."))
            return
        
        # Remove waitee record
        await interaction.response.send_message(ephemeral = True, embed = embeds.Success(f"You will no longer be notified when the server reaches a player count of `{waitee.wants_player_count}`."))
        waitee.delete_instance()
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(WaitingListCog(bot))
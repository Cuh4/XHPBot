# // ---------------------------------------------------------------------
# // ------- [Checks] Bot
# // ---------------------------------------------------------------------

"""
A bunch of slash command checks relating to the bot itself.
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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

from . import CheckFailed
import embeds

# ---- // Main
async def ready(interaction: discord.Interaction):
    """
    Checks if the bot is ready in an app command.

    Args:
        interaction (discord.Interaction): The context of the command.
    """
    
    bot: Bot = interaction.client
    
    if bot.ready:
        return
    else:
        await interaction.response.send_message(ephemeral = True, embed = embeds.Error("🔴 | The bot is not ready."))
        raise CheckFailed("Bot isn't ready")
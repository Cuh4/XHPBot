# // ---------------------------------------------------------------------
# // ------- [Cogs] Statistics Cog
# // ---------------------------------------------------------------------

"""
A cog for tracking server statistics over time.
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
from discord.ext.tasks import loop
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot
    from cogs.status_cog import StatusCog

from cogs.base_cog import BaseCog

from libs import print

import models

# ---- // Main
class StatisticsCog(BaseCog):
    """
    A cog for tracking server statistics over time.
    """
    
    def __init__(self, bot: "Bot"):
        """
        Initializes `StatisticsCog` class objects.
        """        
        
        super().__init__(bot)

        self.statistics_loop = loop(minutes = float(os.getenv("statistics_update_interval")))(self.update_statistics)

    # ---- // Callbacks
    async def cog_start_async(self):
        self.status_cog: "StatusCog" = self.bot.get_cog("StatusCog")
        self.statistics_loop.start()
        
    # ---- // Methods
    async def update_statistics(self):
        """
        Updates server statistics.
        """        
        
        # Get server information
        try:
            server = await self.status_cog.fetch_server_information()
        except Exception as error:
            print.error(self.qualified_name, f"Failed to fetch server information: {error}")
            return
        
        # Update statistics
        try:
            models.ServerStatistic.create_from_server(server)
        except Exception as error:
            print.error(self.qualified_name, f"Failed to update server statistics: {error}")
            
async def setup(bot: "Bot"):
    """
    Sets up the cog.
    Called automatically by `bot.load_extension(...)`.

    Args:
        bot (Bot): The bot to provide to the cog.
    """    
    
    await bot.add_cog(StatisticsCog(bot))
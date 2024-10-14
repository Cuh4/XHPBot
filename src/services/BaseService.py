# // ---------------------------------------------------------------------
# // ------- [Services] Base Service
# // ---------------------------------------------------------------------

"""
A base class for all services.
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
from typing import TYPE_CHECKING

if TYPE_CHECKING: # prevent circular dependency error. we only need this bot impor tfor typechecking anyway
    from bot import Bot

from threading import Thread
from abc import abstractmethod

from libs import print

# ---- // Main
class BaseService():
    """
    Represents a service.
    """
    
    def __init__(self, name: str):
        """
        Initializes `Service` class objects.

        Args:
            name (str): The name of the service.
        """        
        
        self.Name = name
        self.StartThread: Thread = None
        self.Bot: "Bot" = None
        
    async def Start(self, bot: "Bot"):
        """
        Starts this service. Only call this from bot's `on_ready` event.

        Args:
            bot (Bot): The bot to pass to the service.
        """
        
        # Set attributes
        self.Bot = bot
        self.StartThread = Thread(target = self.ServiceStart, args = [bot])
        
        # Print
        print.success("Service", f"Started '{self.Name}'")
        
        # Call methods
        self.StartThread.start()
        await self.ServiceStartAsync(bot)
        
    @abstractmethod
    def ServiceStart(self, bot: "Bot"):
        """
        Called when the service is started (no-async).

        Args:
            bot (Bot): The bot to pass to the service.
        """
    
    @abstractmethod
    async def ServiceStartAsync(self, bot: "Bot"):
        """
        Called when the service is started (async).

        Args:
            bot (Bot): The bot to pass to the service.
        """
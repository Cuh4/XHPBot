# // ---------------------------------------------------------------------
# // ------- [Libs] Archean - Archean
# // ---------------------------------------------------------------------

"""
A module of the Archean package containing the main classes.
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
from __future__ import annotations

import aiohttp
import json
from dataclasses import dataclass

# Exceptions
from . import (
    RequestFailure,
    InvalidJSON,
    InvalidSchema
)

# Enums
from . import (
    Gamemode,
    PasswordProtected
)

# ---- // Main
class Archean():
    """
    A class for interacting with Archean's web API.
    
    >>> archean = Archean()
    >>> server = archean.GetServers()[0]
    >>> print(server.Name)
    """  
  
    def __init__(self):
        """
        Initializes Archean class objects.
        """        
        
        self.URL = "https://api.archean.space/"
        
    async def _Request(self, method: str, endpoint: str) -> any:
        """
        Sends a HTTP request to the Archean API.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The endpoint to send the request to.

        Raises:
            RequestFailure: Raised when a HTTP request to the Archean API fails.
            InvalidJSON: Raised when the Archean API returns invalid JSON.

        Returns:
            requests.Response: The response from the Archean API.
        """        
        
        async with aiohttp.ClientSession() as session:
            response = await session.request(method = method, url = self.URL + endpoint)
            
            if not response.ok:
                raise RequestFailure(f"Response failed with status code {response.status_code}")
            
            try:
                return await response.json()
            except json.decoder.JSONDecodeError as error:
                raise InvalidJSON(f"Invalid JSON: {error}")
        
    async def GetServers(self) -> list[Server]:
        """
        Returns a list of all online Archean servers.

        Returns:
            list[Server]: A list of all online Archean servers.
        """     
        
        servers = await self._Request("GET", "servers")
        
        try:
            servers = servers["servers"]
        except KeyError:
            raise InvalidSchema("Invalid `/servers` response schema")
        
        return [Server._FromDict(server) for server in servers]
    
    async def GetServerByID(self, ID: int) -> Server|None:
        """
        Returns the Archean server with the specified ID.

        Args:
            ID (int): The ID of the Archean server.

        Returns:
            Server|None: The Archean server with the specified ID, or None if not found.
        """     
        
        servers = await self.GetServers()
        
        for server in servers:
            if server.ID != ID:
                continue
            
            return server
        
    async def GetServerByIP(self, IP: str, port: int) -> Server|None:
        """
        Returns the Archean server with the specified IP and port.
        
        Args:
            IP (str): The IP of the Archean server.
            port (int): The port of the Archean server.
            
        Returns:
            Server|None: The Archean server with the specified IP and port, or None if not found.
        """
        
        servers = await self.GetServers()
        
        for server in servers:
            if server.IP != IP or server.Port != port:
                continue
            
            return server
        
    async def GetServersByGamemode(self, gamemode: Gamemode) -> list[Server]:
        """
        Returns a list of servers with a specific gamemode.

        Args:
            gamemode (Gamemode): The gamemode to filter by.

        Returns:
            list[Server]: A list of servers with the specified gamemode.
        """        
        
        servers = await self.GetServers()
        return [server for server in servers if server.Gamemode == gamemode]
    
    async def GetServersWithPassword(self, passwordProtected: PasswordProtected) -> list[Server]:
        """
        Returns a list of servers with a specific password protection status.

        Args:
            passwordProtected (PasswordProtected): The password protection status to filter by.

        Returns:
            list[Server]: A list of servers with the specified password protection status.
        """        
        
        servers = await self.GetServers()
        return [server for server in servers if server.PasswordProtected == passwordProtected]
        
@dataclass
class Server():
    @staticmethod
    def _FromDict(data: dict) -> Server:
        return Server(
            ID = data["id"],
            Name = data["name"],
            IP = data["host"],
            Port = data["port"],
            Branch = data["branch"],
            Players = data["nb_players"],
            MaxPlayers = data["max_players"],
            Gamemode = Gamemode(data["mode"]),
            PasswordProtected = PasswordProtected(data["pswd"]),
            Version = data["version"]
        )
    
    ID: int
    Name: str
    IP: str
    Port: int
    Branch: str
    Players: int
    MaxPlayers: int
    Gamemode: Gamemode
    PasswordProtected: PasswordProtected
    Version: int
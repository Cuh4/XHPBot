# // ---------------------------------------------------------------------
# // ------- [Libs] Archean - Archean
# // ---------------------------------------------------------------------

"""
A module of the Archean package containing the main classes.
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
from __future__ import annotations

import os
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
    >>> server = archean.get_servers()[0]
    >>> print(server.name)
    """  
  
    def __init__(self):
        """
        Initializes Archean class objects.
        """        
        
        self.url = "https://api.archean.space/"
        
    async def _request(self, method: str, endpoint: str) -> any:
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
            response = await session.request(method = method, url = self.url + endpoint, headers = {
                "User-Agent": f"{os.getenv("github_repo_url").replace("https://github.com/", "")} ({os.getenv("github_repo_url")})"
            })
            
            if not response.ok:
                raise RequestFailure(f"Response failed with status code {response.status_code}")
            
            try:
                return await response.json()
            except json.decoder.JSONDecodeError as error:
                raise InvalidJSON(f"Invalid JSON: {error}")
        
    async def get_servers(self) -> list[Server]:
        """
        Returns a list of all online Archean servers.

        Returns:
            list[Server]: A list of all online Archean servers.
        """     
        
        servers = await self._request("GET", "servers")
        
        try:
            servers = servers["servers"]
        except KeyError:
            raise InvalidSchema("Invalid `/servers` response schema")
        
        return [Server._from_dict(server) for server in servers]
    
    async def get_server_by_id(self, id: int) -> Server|None:
        """
        Returns the Archean server with the specified ID.

        Args:
            id (int): The ID of the Archean server.

        Returns:
            Server|None: The Archean server with the specified ID, or None if not found.
        """     
        
        servers = await self.get_servers()
        
        for server in servers:
            if server.id != id:
                continue
            
            return server
        
    async def get_server_by_ip(self, ip: str, port: int) -> Server|None:
        """
        Returns the Archean server with the specified IP and port.
        
        Args:
            ip (str): The IP of the Archean server.
            port (int): The port of the Archean server.
            
        Returns:
            Server|None: The Archean server with the specified IP and port, or None if not found.
        """
        
        servers = await self.get_servers()
        
        for server in servers:
            if server.ip != ip or server.port != port:
                continue
            
            return server
        
    async def get_servers_by_gamemode(self, gamemode: Gamemode) -> list[Server]:
        """
        Returns a list of servers with a specific gamemode.

        Args:
            gamemode (Gamemode): The gamemode to filter by.

        Returns:
            list[Server]: A list of servers with the specified gamemode.
        """        
        
        servers = await self.get_servers()
        return [server for server in servers if server.gamemode == gamemode]
    
    async def get_servers_by_password(self, password_protected: PasswordProtected) -> list[Server]:
        """
        Returns a list of servers with a specific password protection status.

        Args:
            password_protected (PasswordProtected): The password protection status to filter by.

        Returns:
            list[Server]: A list of servers with the specified password protection status.
        """        
        
        servers = await self.get_servers()
        return [server for server in servers if server.password_protected == password_protected]
        
@dataclass
class Server():
    id: int
    name: str
    ip: str
    port: int
    branch: str
    players: int
    max_players: int
    gamemode: Gamemode
    password_protected: PasswordProtected
    version: int

    @classmethod
    def _from_dict(cls, data: dict) -> Server:
        """
        Creates a server from a dictionary.

        Args:
            data (dict): The dictionary to create the server from.
            
        Returns:
            Server: The created server.
        """
        
        return cls(
            id = data["id"],
            name = data["name"],
            ip = data["host"],
            port = data["port"],
            branch = data["branch"],
            players = data["nb_players"],
            max_players = data["max_players"],
            gamemode = Gamemode(data["mode"]),
            password_protected = PasswordProtected(data["pswd"]),
            version = data["version"]
        )
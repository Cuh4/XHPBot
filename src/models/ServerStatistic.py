# // ---------------------------------------------------------------------
# // ------- [Models] Server Statistic
# // ---------------------------------------------------------------------

"""
A model containing statistics for the XHP server at a given time.
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

import peewee
import time

from libs.archean import Server
from . import proxy

# ---- // Main
class ServerStatistic(peewee.Model):
    """
    A model containing data for server status, etc.
    """

    ID = peewee.IntegerField(primary_key = True, unique = True)
    Time = peewee.FloatField(default = time.time)
    PlayerCount = peewee.IntegerField()
    MaxPlayers = peewee.IntegerField()
    Version = peewee.TextField()
    
    class Meta:
        database = proxy
        
    @classmethod
    def get_peak_player_count(cls) -> ServerStatistic|None:
        try:
            return cls.select().order_by(cls.PlayerCount).limit(1).get()
        except peewee.DoesNotExist:
            return None
        
    @classmethod
    def create_from_server(cls, server: Server) -> ServerStatistic:
        """
        Creates a ServerStatistic object and saves to the database from an Archean Server object.

        Args:
            server (Server): The Archean Server object.
            
        Returns:
            ServerStatistic: The created and stored ServerStatistic object.
        """
        
        return cls.create(
            PlayerCount = server.Players,
            MaxPlayers = server.MaxPlayers,
            Version = server.Version
        )
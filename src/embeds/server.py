# // ---------------------------------------------------------------------
# // ------- [Embeds] Server
# // ---------------------------------------------------------------------

"""
An embed for displaying information on an Archean server.
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
import os

import models

from libs.archean import Server as ArcheanServer
from libs.archean import PasswordProtected
from libs.timestamp import timestamp
from libs.server import get_server_ip

# ---- // Main
class Server(discord.Embed):
    """
    An embed displaying information on a server.
    """
    
    def __init__(self, server: ArcheanServer|None):
        """
        An embed displaying information on a server.

        Args:
            server (ArcheanServer|None): The server to show information on.
        """
        
        super().__init__()
        
        if server:
            peak = models.ServerStatistic.get_peak_player_count()
            
            if peak is None:
                self.title = "Error"
                self.description = "No server statistics. This should fix itself on its own."
                self.color = discord.Color.from_rgb(200, 125, 125)
                
                return
            
            self.title = f"☀️ | {server.name}"

            self.description = "\n".join([
                # 1st row
                f"🗻 | **{str(server.gamemode).capitalize()} Mode**" + " • "
                    + f"🔗 | {get_server_ip(server) or "IP Hidden"} • "
                    + ("🔒 | **Password Protected**" if server.password_protected == PasswordProtected.PROTECTED else "🔓 | **No Password**"),
                    
                # Separator
                "",

                # 2nd-3rd row
                "🟢 | **Online**",
                f"👥 | `{server.players}`/`{server.max_players}` **Players**",
                f"🔥 | **Peak: {timestamp(peak.time, "R")} with** `{peak.player_count}/{peak.max_players}` **players.**"
            ])
            
            self.color = discord.Color.from_rgb(125, 200, 125)
            
            self.set_footer(text = f"Server Version: v{server.version}")
            self.set_image(url = os.getenv("status_banner"))
        else:
            self.title = "Server"
            self.description = f"⛔ | The server is offline."
            self.color = discord.Color.red()
            
        self.description += f"\n-# Refreshes every {float(os.getenv("status_update_interval")):.1f} seconds"
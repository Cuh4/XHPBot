# // ---------------------------------------------------------------------
# // ------- [Embeds] Compact Server
# // ---------------------------------------------------------------------

"""
An embed for displaying information on an Archean server. This embed is compact compared to the other one.
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

from libs.archean import (
    Server,
    PasswordProtected
)

# ---- // Main
class CompactServer(discord.Embed):
    """
    An embed displaying information on a server.
    """
    
    def __init__(self, server: Server|None):
        """
        An embed displaying information on a server.

        Args:
            server (Server|None): The server to show information on.
        """
        
        super().__init__()
        
        if server:
            self.title = f"☀️ | {server.name}"

            self.description = "\n".join([
                # 1st row
                (f"**⚙️ | {str(server.gamemode).capitalize()}**") + " • "
                    + f"🔗 | " + (f"**{server.ip}:{server.port}**" if os.getenv("status_hide_ip") != "yes" else "**IP Hidden**") + " • "
                    + ("**🔒 | Password Protected**" if server.password_protected == PasswordProtected.PROTECTED else "**🔓 | No Password**"),

                # 2nd row
                f"👥 | `{server.players}/{server.max_players}` **Players**",
            ])
            
            self.color = discord.Color.from_rgb(125, 200, 125)
        else:
            self.title = "Server"
            self.description = f"⛔ | The server is offline."
            self.color = discord.Color.red()
# // ---------------------------------------------------------------------
# // ------- [Embeds] Compact Server
# // ---------------------------------------------------------------------

"""
An embed for displaying information on an Archean server. This embed is compact compared to the other one.
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

from libs.archean import (
    Server,
    PasswordProtected
)

from libs import env

# ---- // Main
def embed(server: Server) -> discord.Embed:
    """
    Returns an embed that shows compacted information on an Archean server.

    Args:
        server (Server): The server to show information on.

    Returns:
        discord.Embed: The created embed.
    """    
    
    if server:
        embed = discord.Embed(
            title = f"☀️ | {server.Name}",

            description = "\n".join([
                f"**⚙️ | {server.Gamemode}**",
                "🔒 | Password Protected" if server.PasswordProtected == PasswordProtected.Protected else "🔓 | No Password",
                f"👥 | {server.Players}/{server.MaxPlayers} Players",
            ]),
            
            color = env.GetStatusEmbedColor()
        )
    else:
        embed = discord.Embed(
            title = "Server",
            description = f"⛔ | The server is offline.",
            color = discord.Color.red()
        )
        
    return embed
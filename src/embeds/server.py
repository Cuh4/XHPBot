# // ---------------------------------------------------------------------
# // ------- [Embeds] Server
# // ---------------------------------------------------------------------

"""
An embed for displaying information on an Archean server.
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
    Returns an embed that shows information on an Archean server.

    Args:
        server (Server): The server to show information on.

    Returns:
        discord.Embed: The created embed.
    """    
    
    if server:
        embed = discord.Embed(
            title = f"☀️ | {server.Name}",

            description = "\n".join([
                f"**⚙️ | {server.Gamemode} Server • " + ("🔒 | Password Protected" if server.PasswordProtected == PasswordProtected.Protected else "🔓 | No Password") + "**",
                f"🔗 | " + (f"{server.IP}:{server.Port}" if not env.GetHideIP() else "IP Hidden"),
                f"👥 | {server.Players}/{server.MaxPlayers} Players",
                f"-# Refreshes every {env.GetStatusRefreshRate():.1f} seconds",
            ]),
            
            color = env.GetStatusEmbedColor()
        )
        
        embed.set_footer(text = f"Server Version: v{server.Version}")
        embed.set_image(url = env.GetStatusBannerURL())
    else:
        embed = discord.Embed(
            title = "Server",
            description = f"⛔ | The server is offline.\n-# Last updated: {lastUpdated}",
            color = discord.Color.red()
        )
        
    return embed
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
import os

import models

from libs.archean import (
    Server,
    PasswordProtected
)

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
        peak = models.ServerStatistic.get_peak_player_count()
        
        embed = discord.Embed(
            title = f"☀️ | {server.Name}",

            description = "\n".join([
                f"🗻 | {server.Gamemode}",
                "🔒 | Password Protected" if server.PasswordProtected == PasswordProtected.Protected else "🔓 | No Password",
                f"🔗 | " + (f"`{server.IP}:{server.Port}`" if os.getenv("status_hide_ip") != "yes" else "IP Hidden"),
                f"👥 | `{server.Players}`/`{server.MaxPlayers}` Players",
                f"🔥 | Peak Player Count: {f"<t:{int(peak.Time)}:R> with `{peak.PlayerCount}/{peak.MaxPlayers}` players." if peak else "N/A"}"
            ]),
            
            color = discord.Color.from_rgb(125, 200, 125)
        )
        
        embed.set_footer(text = f"Server Version: v{server.Version}")
        embed.set_image(url = os.getenv("status_banner"))
    else:
        embed = discord.Embed(
            title = "Server",
            description = f"⛔ | The server is offline.",
            color = discord.Color.red()
        )
        
    embed.description += f"\n-# Refreshes every {float(os.getenv("status_update_interval")):.1f} seconds"
    return embed
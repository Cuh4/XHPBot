# // ---------------------------------------------------------------------
# // ------- [Embeds] Error
# // ---------------------------------------------------------------------

"""
An error embed.
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

# ---- // Main
def embed(text: str, title: str = None, imgBanner: str = None, imgIcon: str = None) -> discord.Embed:
    """
    Returns an error embed.

    Args:
        text (str): The text to display.
        title (str): The title of the embed.
        imgBanner (str): The banner image URL.
        imgIcon (str): The icon image URL.

    Returns:
        Embed: The error embed.
    """
    
    return discord.Embed(
        title = title,
        description = text,
        color = discord.Color.from_rgb(255, 125, 125)
    ).set_thumbnail(url = imgIcon).set_image(url = imgBanner)
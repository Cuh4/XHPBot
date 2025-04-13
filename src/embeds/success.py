# // ---------------------------------------------------------------------
# // ------- [Embeds] Success
# // ---------------------------------------------------------------------

"""
A success embed.
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
from . import Info

# ---- // Main
class Success(Info):
    """
    Represents a success embed.
    """
    
    def __init__(self, text: str, title: str = None, img_banner: str = None, img_icon: str = None):
        """
        Represents a success embed.

        Args:
            text (str): The text to display.
            title (str): The title of the embed.
            img_banner (str): The banner image URL.
            img_icon (str): The icon image URL.
        """
        
        super().__init__(text = text, title = title, img_banner = img_banner, img_icon = img_icon)
        self.color = discord.Color.from_rgb(125, 255, 125)
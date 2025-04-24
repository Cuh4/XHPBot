# // ---------------------------------------------------------------------
# // ------- [Embeds] Live Chat
# // ---------------------------------------------------------------------

"""
An embed representing a live chat message
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
from discord import Embed, Color

# ---- // Main
class LiveChat(Embed):
    """
    An embed representing a live chat message
    """
    
    def __init__(self, title: str, text: str, color: tuple[int, int, int] = (255, 255, 255), emoji: str = "💬"):
        """
        Initializes `LiveChat` class instances.

        Args:
            title (str): The title of the embed.
            text (str): The text of the embed.
            color (tuple[int, int, int], optional): The color of the embed. Defaults to (255, 255, 255).
            emoji (str, optional): The emoji to use in the embed. Defaults to "💬".
        """
        
        super().__init__(
            description = f"{emoji} | `{title.replace("`", "\\`")}` | {text}",
            color = Color.from_rgb(*color)
        )
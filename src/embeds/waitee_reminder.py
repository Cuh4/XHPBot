# // ---------------------------------------------------------------------
# // ------- [Embeds] Waitee
# // ---------------------------------------------------------------------

"""
An embed representing a reminder for a Waitee.
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
from . import Success
from libs import timestamp
from models import Waitee

# ---- // Main
class WaiteeReminder(Success):
    """
    An embed representing a reminder for a Waitee.
    """
    
    def __init__(self, waitee: Waitee, used_fallback = False):
        """
        An embed representing a reminder for a Waitee.

        Args:
            waitee (Waitee): The Waitee.
            used_fallback (bool, optional): Whether or not a fallback channel was used. Defaults to False.
        """
        
        super().__init__(
            title = "Reminder",
            text = "\n".join([
                f"**The server has reached a player count of `{waitee.wants_player_count}`**.",
                "You will not be reminded again unless you use `/wait` again.",
                "",
                "-# This message was sent because you wanted to be notified about this " + timestamp.timestamp(waitee.start_time, "R") + "."
            ])
        )
        
        if used_fallback:
            self.description += "\n-# ⚠️ - We couldn't remind you through DMs, so this reminder was sent here instead."
# // ---------------------------------------------------------------------
# // ------- [Libs] Timestamp
# // ---------------------------------------------------------------------

"""
A module for interacting with Discord timestamps.
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

# ---- // Main
def FormatTimestamp(timestamp: int|float, mode: str) -> str:
    """
    Formats a timestamp into a Discord timestamp.

    Args:
        timestamp (int | float): The timestamp to format.
        mode (str): The mode to format the timestamp in.

    Returns:
        str: The formatted timestamp.
    """
    
    return f"<t:{int(timestamp)}:{mode}>"
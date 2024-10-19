# // ---------------------------------------------------------------------
# // ------- [Libs] Archean - Enums
# // ---------------------------------------------------------------------

"""
A module containing exceptions raised during failures.
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
from enum import Enum

# ---- // Main
class Gamemode(Enum):
    """
    The gamemode of a server.
    """
    
    CREATIVE = 0
    ADVENTURE = 1
    SURVIVAL = 2
    
    def __str__(self) -> str:
        return self.name
    
class PasswordProtected(Enum):
    """
    Whether or not a server is password protected.
    """
    
    UNPROTECTED = 0
    PROTECTED = 1
    
    def __str__(self) -> str:
        return self.name
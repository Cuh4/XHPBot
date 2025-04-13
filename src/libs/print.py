# // ---------------------------------------------------------------------
# // ------- [Libs] Print
# // ---------------------------------------------------------------------

"""
A module for printing messages in a neat format.
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
import colorama
from colorama import Fore, Back
from datetime import datetime

# ---- // Variables
MAX_TITLE_LENGTH = 15

# ---- // Main
colorama.init()

def _print(title: str, color: str, *args, separator: str = " "):
    """
    Prints a message in a neat format.

    Args:
        title (str): The title of the message.
        color (str): The color of the message.
        separator (str, optional): The separator used between the provided args. Defaults to " ".
    """
    
    args = [str(arg) for arg in args]
    
    if len(title) > MAX_TITLE_LENGTH:
        title = title[:MAX_TITLE_LENGTH - 3] + "..."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spacing = " " * (MAX_TITLE_LENGTH - len(title))
    
    print(f"{Back.BLACK}{color}{now}{Back.RESET}{spacing}{title}{Fore.RESET}: {separator.join(args)}")
    
def success(title: str, *args, **kwargs):
    """
    Prints a success message.

    Args:
        title (str): The title of the message.
    """

    _print(title, Fore.GREEN, *args, **kwargs)
    
def error(title: str, *args, **kwargs):
    """
    Prints an error message.

    Args:
        title (str): The title of the message.
    """

    _print(title, Fore.RED, *args, **kwargs)
    
def info(title: str, *args, **kwargs):
    """
    Prints an info message.

    Args:
        title (str): The title of the message.
    """

    _print(title, Fore.BLUE, *args, **kwargs)
    
def warning(title: str, *args, **kwargs):
    """
    Prints a warning message.

    Args:
        title (str): The title of the message.
    """

    _print(title, Fore.YELLOW, *args, **kwargs)
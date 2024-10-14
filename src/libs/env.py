# // ---------------------------------------------------------------------
# // ------- [Libs] Env
# // ---------------------------------------------------------------------

"""
A module for reading user config.
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
from dotenv import load_dotenv
import os

from discord import Color

# ---- // Main
load_dotenv()

def GetBotToken() -> str:
    """
    Returns the bot token from the .env file.

    Raises:
        EnvironmentError: The bot token is not set in the .env file.

    Returns:
        str: The bot token.
    """    
    
    botToken = os.getenv("bot_token")
    
    if botToken == "":
        raise EnvironmentError("The bot token is not set in the .env file. Please make a bot at https://discord.com/developers/applications and plop the token in the .env file.")
    
    return botToken

def GetServerIP() -> tuple[str, int]:
    """
    Returns the server IP from the .env file.

    Raises:
        EnvironmentError: The server IP is not set in the .env file or is in an invalid format.
        EnvironmentError: The port portion of the server IP in the .env file is invalid.

    Returns:
        str: The server IP.
        int: The server port.
    """
    
    raw = os.getenv("server_ip")
    
    if raw == "" or len(raw.split(":")) != 2:
        raise EnvironmentError("The server IP is not set in the .env file or is in an invalid format (should be IP:Port). Please set the server IP correctly in the .env file.")
    
    serverIP, serverPort = raw.split(":")
    
    if not serverPort.isnumeric() or not serverPort.isdecimal():
        raise EnvironmentError("The port portion of the server IP in the .env file is invalid. Ensure it is a number.")
    
    return serverIP, int(serverPort)

def GetRefreshRate() -> float:
    """
    Returns the refresh rate from the .env file.

    Raises:
        EnvironmentError: The refresh rate is not set in the .env file or is in an invalid format.

    Returns:
        float: The refresh rate.
    """    
    
    refreshRate = os.getenv("refresh_rate")
    
    if not refreshRate.isnumeric() or not refreshRate.isdecimal():
        raise EnvironmentError("The refresh rate is not set in the .env file or is in an invalid format. Please set the refresh rate correctly in the .env file.")
    
    return float(refreshRate)

def GetDatabasePath() -> str:
    """
    Returns the database path from the .env file.

    Raises:
        EnvironmentError: The database path is not set in the .env file.

    Returns:
        str: The database path.
    """    
    
    databasePath = os.getenv("db_path")
    
    if databasePath == "":
        raise EnvironmentError("The database path is not set in the .env file. Please set the database path correctly in the .env file.")
    
    if databasePath is None:
        raise EnvironmentError("The database path is not set in the .env file. Please set the database path correctly in the .env file.")
    
    return databasePath

def GetStatusChannel() -> int:
    """
    Returns the status channel ID from the .env file.

    Raises:
        EnvironmentError: The status channel ID is not set in the .env file.

    Returns:
        int: The status channel ID.
    """    
    
    statusChannel = os.getenv("status_channel")
    
    if statusChannel is None or statusChannel == "":
        raise EnvironmentError("The status channel ID is not set in the .env file. Please set the status channel ID correctly in the .env file.")
    
    if not statusChannel.isnumeric():
        raise EnvironmentError("The status channel ID is not an ID. Please set the status channel ID correctly in the .env file.")
    
    return int(statusChannel)

def GetStatusEmbedColor() -> Color:
    """
    Returns the status embed color from the .env file.

    Raises:
        EnvironmentError: The status embed color is not set in the .env file or is incorrectly formatted.

    Returns:
        Color: The status embed color.
    """    
    
    color = os.getenv("status_embed_color")
    
    if color is None:
        raise EnvironmentError("The status embed color is not set in the .env file. Please set the status embed color correctly in the .env file.")
    
    if len(color.split(",")) < 3 or len(color.split(",")) > 3:
        raise EnvironmentError("The status embed color in the .env is incorrectly formatted. Use the format 'r,g,b'.")
    
    r, g, b = color.split(",")
    
    if not r.isnumeric() or not g.isnumeric() or not b.isnumeric():
        raise EnvironmentError("The status embed color in the .env is incorrectly formatted. Use the format 'r,g,b' and ensure all values are integers.")
    
    return Color.from_rgb(int(r), int(g), int(b))

def GetStatusBannerURL() -> str:
    """
    Returns the status banner from the .env file.

    Returns:
        str: The status banner URL.
    """
    
    return os.getenv("status_banner") or ""

def GetHideIP() -> bool:
    """
    Returns whether or not to hide the server IP in the server status message. Gathered from the .env file.

    Returns:
        bool: Whether or not to hide the IP
    """
    
    return os.getenv("hide_ip") == "yes"

def GetGitHubRepoURL() -> str:
    """
    Returns the GitHub repo URL from the .env file.

    Returns:
        str: The GitHub repo URL.
    """
    
    return os.getenv("github_repo_url")
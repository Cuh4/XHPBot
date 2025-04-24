# // ---------------------------------------------------------------------
# // ------- [Libs] Server
# // ---------------------------------------------------------------------

"""
A module for server-related functions.
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
import os

from libs.archean import Server

# ---- // Main
def get_our_server_ip() -> str|None:
    """
    Returns the server's formatted IP address.
    
    Returns:
        str: The server IP address.
    """
    
    our_server_ip = os.getenv("server_ip")
    hide_ip = os.getenv("status_hide_ip").lower() == "yes"
    
    if hide_ip:
        return None
    
    domain = os.getenv("server_domain")
    
    if domain != "":
        port = our_server_ip.split(":")[1]
        return f"{domain}:{port}"
    
    return our_server_ip

def get_server_ip(server: Server) -> str|None:
    """
    Returns the server's formatted IP address.

    Args:
        server (Server): The server full IP to return.

    Returns:
        str: The server IP address.
    """
    
    our_server_ip = os.getenv("server_ip")
    
    if server is None:
        return get_our_server_ip()
    
    full_server_ip = f"{server.ip}:{server.port}"
    
    if full_server_ip != our_server_ip:
        return full_server_ip
    
    return get_our_server_ip()
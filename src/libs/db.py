# // ---------------------------------------------------------------------
# // ------- [Libs] DB
# // ---------------------------------------------------------------------

"""
A module for handling basic data persistence via JSON.
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
import json
import os

# ---- // Main
class Database():
    """
    A class for handling basic data persistence via JSON.
    """    
    
    def __init__(self, path: str, default: dict = {}):
        """
        Initializes the database.

        Args:
            path (str): The path to the JSON file (eg: "C:/Main/db.json")
            default (dict, optional): The default data in case the .JSON file doesn't exist. Defaults to {}
        """
        
        self.Path = path
        self.Default = default
        self.Data = self.Default
    
        self.Load()
        
    def _EnsurePathExists(self):
        """
        Creates the directory for the JSON file if it doesn't exist.
        """
        
        path = os.path.dirname(self.Path)
        
        try:
            os.makedirs(path, exist_ok = True)
        except FileNotFoundError:
            return
        
    def Save(self, data: dict):
        """
        Saves the data to the JSON file.

        Args:
            data (dict): The data to save
        """
        
        self._EnsurePathExists()
        
        with open(self.Path, "w") as file:
            json.dump({**self.Data, **data}, file, indent = 4)
            
    def Load(self) -> dict:
        """
        Loads the data from the JSON file.

        Returns:
            dict: The data from the JSON file
        """
        
        try:
            with open(self.Path, "r") as file:
                decoded = {**json.loads(file.read())}
                data = {**self.Default, **decoded}
                
                if data != decoded: # again if values were missing, save
                    self.Save(data)
                
                self.Data = data
                return self.Data
        except json.decoder.JSONDecodeError:
            self.Save(self.Default)
            return self.Default
        except FileNotFoundError:
            self.Save(self.Default)
            return self.Default
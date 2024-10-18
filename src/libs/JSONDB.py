# // ---------------------------------------------------------------------
# // ------- [Libs] JSONDB
# // ---------------------------------------------------------------------

"""
A module for storing values in a JSON database.
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
class SchemaValue():
    """
    Represents a value in a JSON database schema.
    """
    
    def __init__(self, *, valueType: any, default: any):
        """
        Represents a value in a JSON database schema.

        Args:
            valueType (any): The type of the value.
            default (any): The default value to use if the value doesn't exist in the database.

        Raises:
            SchemaError: If the value type doesn't match the default provided.
        """
        
        if type(default) != valueType:
            raise SchemaError(f"Invalid default type for schema value: {type(default)} != {valueType}")
        
        self.Type = valueType
        self.Default = default
        

class Database():
    """
    A class for storing values into a JSON database.
    """
    
    def __init__(self, path: str):
        """
        A class for storing values into a JSON database.

        Args:
            path (str): The path to the JSON database.
        """        
        
        self.Path = path
        self.Schema: dict[str, SchemaValue] = {}
        self.Data = {}
        
        try:
            self._Load()
        except:
            self._Validate()
            self._Save()
            
    def _CreatePath(self):
        """
        Creates the path to the JSON database file.
        """
        
        path = os.path.dirname(self.Path)
        
        if path == "":
            return
        
        if not os.path.exists(path):
            os.makedirs(path)
        
    def _Load(self):
        """
        Loads the database.
        """
        
        try:
            self._CreatePath()
            
            with open(self.Path, "r") as file:
                data = json.load(file)
                self.Data = data
                self._Validate()
        except Exception as error:
            raise DatabaseError(f"Failed to load database: {error}")
        
    def _Save(self):
        """
        Saves the database.
        """
        
        try:
            with open(self.Path, "w") as file:
                json.dump(self.Data, file, indent = 7)
        except Exception as error:
            raise DatabaseError(f"Failed to save database: {error}")
        
    def _Validate(self):
        """
        Iterates through the schema and validates each value in the database by matching with the schema.
        """
        
        for index, schemaValue in self.Schema.items():
            savedValue = self.Data.get(index)
            
            if type(savedValue) == schemaValue.Type:
                continue
            
            self.Data[index] = schemaValue.Default
            
    def GetSchemaValue(self, index: str) -> SchemaValue:
        return self.Schema.get(index)
        
    def SetSchema(self, schema: dict[str, SchemaValue]):
        """
        Sets the schema for this database.
        
        >>> JSONDB = Database("db.json")
        >>> 
        >>> JSONDB.SetSchema({
        >>>     "last_updated" : JSONSchemaValue(valueType = int, default = 0),
        >>>     "foo" : JSONSchemaValue(valueType = str, default = "bar")
        >>> })

        Args:
            schema (dict): The schema to use.
        """        
        
        self.Schema = schema
        
    def Set(self, index: str, value: any):
        """
        Sets a value in the database.

        Args:
            index (str): The index of the value to set.
            value (any): The value to set.
        """
        
        schemaValue = self.GetSchemaValue(index)
        
        if schemaValue is None:
            raise DatabaseError(f"Invalid index (not in schema): {index}")
        
        if type(value) != schemaValue.Type:
            raise DatabaseError(f"Invalid value type: {type(value)} != {schemaValue.Type}")
        
        self.Data[index] = value
        self._Save()
        
    def Get(self, index: str) -> any:
        """
        Returns a value from the database.
        
        Args:
            index (str): The index of the value to get.
            
        Returns:
            any: The value from the database.
        """
        
        schemaValue = self.GetSchemaValue(index)
        
        if schemaValue is None:
            raise DatabaseError(f"Invalid index (not in schema): {index}")
        
        value = self.Data.get(index)
        
        if type(value) != schemaValue.Type:
            self._Validate()
            value = schemaValue.Default
        
        return value
        
class DatabaseError(Exception):
    pass

class SchemaError(Exception):
    pass
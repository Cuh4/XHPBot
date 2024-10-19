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
    
    def __init__(self, *, value_type: any, default: any):
        """
        Represents a value in a JSON database schema.

        Args:
            value_type (any): The type of the value.
            default (any): The default value to use if the value doesn't exist in the database.

        Raises:
            SchemaError: If the value type doesn't match the default provided.
        """
        
        if type(default) != value_type:
            raise SchemaError(f"Invalid default type for schema value: {type(default)} != {value_type}")
        
        self.type = value_type
        self.default = default
        

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
        
        self.path = path
        self.schema: dict[str, SchemaValue] = {}
        self.data = {}
        
        try:
            self._load()
        except:
            self._validate()
            self._save()
            
    def _create_path(self):
        """
        Creates the path to the JSON database file.
        """
        
        path = os.path.dirname(self.path)
        
        if path == "":
            return
        
        if not os.path.exists(path):
            os.makedirs(path)
        
    def _load(self):
        """
        Loads the database.
        """
        
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                self.data = data
                self._validate()
        except Exception as error:
            raise DatabaseError(f"Failed to load database: {error}")
        
    def _save(self):
        """
        Saves the database.
        """
        
        try:
            self._create_path()
            
            with open(self.path, "w") as file:
                json.dump(self.data, file, indent = 7)
        except Exception as error:
            raise DatabaseError(f"Failed to save database: {error}")
        
    def _validate(self):
        """
        Iterates through the schema and validates each value in the database by matching with the schema.
        """
        
        for index, schema_value in self.schema.items():
            saved_value = self.data.get(index)
            
            if type(saved_value) == schema_value.type:
                continue
            
            self.data[index] = schema_value.default
            
    def get_schema_value(self, index: str) -> SchemaValue:
        return self.schema.get(index)
        
    def set_schema(self, schema: dict[str, SchemaValue]):
        """
        Sets the schema for this database.
        
        >>> json_db = Database("db.json")
        >>> 
        >>> json_db.set_schema({
        >>>     "last_updated" : JSONSchemaValue(value_type = int, default = 0),
        >>>     "foo" : JSONSchemaValue(value_type = str, default = "bar")
        >>> })

        Args:
            schema (dict): The schema to use.
        """        
        
        self.schema = schema
        
    def set(self, index: str, value: any):
        """
        Sets a value in the database.

        Args:
            index (str): The index of the value to set.
            value (any): The value to set.
        """
        
        schema_value = self.get_schema_value(index)
        
        if schema_value is None:
            raise DatabaseError(f"Invalid index (not in schema): {index}")
        
        if type(value) != schema_value.type:
            raise DatabaseError(f"Invalid value type: {type(value)} != {schema_value.type}")
        
        self.data[index] = value
        self._save()
        
    def get(self, index: str) -> any:
        """
        Returns a value from the database.
        
        Args:
            index (str): The index of the value to get.
            
        Returns:
            any: The value from the database.
        """
        
        schema_value = self.get_schema_value(index)
        
        if schema_value is None:
            raise DatabaseError(f"Invalid index (not in schema): {index}")
        
        value = self.data.get(index)
        
        if type(value) != schema_value.type:
            self._validate()
            value = schema_value.default
        
        return value
        
class DatabaseError(Exception):
    pass

class SchemaError(Exception):
    pass
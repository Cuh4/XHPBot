# // ---------------------------------------------------------------------
# // ------- [Models] Init
# // ---------------------------------------------------------------------

"""
A collection of Peewee database models.
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
import peewee
proxy = peewee.DatabaseProxy()

from .ServerStatistic import ServerStatistic

# ---- // Variables
all = [model for model in locals().values() if isinstance(model, peewee.ModelBase)]

# ---- // Functions
def latch(database: peewee.Database, tables: list[peewee.ModelBase]):
    """
    Initializes the database proxy and creates tables.

    Args:
        database (peewee.Database): The database to use.
        tables (list[peewee.ModelBase]): The tables to create.
    """
    
    proxy.initialize(database)
    database.create_tables(tables)
# // ---------------------------------------------------------------------
# // ------- XHP Inc. Bot
# // ---------------------------------------------------------------------

"""
A Discord bot for the XHP Inc. server.
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
from playhouse.sqliteq import SqliteQueueDatabase
import os
from dotenv import load_dotenv

import models
import libs.print as print
import libs.json_db as json_db
from bot import Bot

# ---- // Main
# Load .env
load_dotenv()

# Create databases
sql_database = SqliteQueueDatabase(os.getenv("sqldb_path"))
models.latch(sql_database, models.all)

print.success("Database", "Created tables for models: " + ", ".join([model.__name__ for model in models.all]))

json_database = json_db.Database(os.getenv("jsondb_path"))
json_database.set_schema({
    "status_message_id" : json_db.SchemaValue(value_type = int, default = 0)
})

# Create bot
bot = Bot(sql_database = sql_database, json_database = json_database)

# Run bot
bot.run(token = os.getenv("bot_token"))
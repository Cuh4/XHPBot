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
import libs.env as env

from jsonstore import JsonStore

from bot import Bot

# ---- // Main
# Create database
database = JsonStore(path = env.GetDatabasePath(), indent = 7)

# Create bot
bot = Bot(database = database)

# Run bot
bot.run(token = env.GetBotToken())
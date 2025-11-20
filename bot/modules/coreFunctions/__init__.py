from importlib import import_module
from sys import argv

# checks if the user wants to update the database or start the bot
database_update = True
if len(argv) > 1:
    if argv[1] == "-start":
        database_update = False

if not database_update:
    this_module = import_module(".coreFunctions.commands", "modules")
    handlers = [this_module.coreFunctions_start_handler]
else:
    commands_defaults = [
        {
            "command_id": "coreFunctions_start",
            "command_handler": "start",
            "command_description": "Send an introduction to the bot",
            "scope": "default",
            "messages": [
                {
                    "message_id": "coreFunctions_start_message",
                    "message": "Hello! I'm a bot, you probably already knew that...",
                }
            ],
        }
    ]

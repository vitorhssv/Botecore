from importlib import import_module
from sys import argv

# checks if the user wants to update the database or start the bot
database_update = True
if len(argv) > 1:
    if argv[1] == "-start":
        database_update = False

if not database_update:
    this_module = import_module(".coreFunctions.commands", "modules")
    handlers = [
        this_module.start_handler,
        this_module.set_commands_handler,
        this_module.reset_commands_handler,
        this_module.restart_handler,
    ]
else:
    commands_defaults = [
        {
            "command_id": "coreFunctions:start",
            "command_handler": "start",
            "command_description": "Send an introduction to the bot",
            "command_scope": "default",
            "messages": [
                {
                    "message_id": "coreFunctions:start_message",
                    "message": "Hello! I'm a bot, you probably already knew that...",
                }
            ],
        },
        {
            "command_id": "coreFunctions:set_commands",
            "command_handler": "set_commands",
            "command_description": "Set the bot's commands",
            "command_scope": "ownerOnly",
            "messages": [
                {
                    "message_id": "coreFunctions:set_commands_complete",
                    "message": "The commands menu was updated!",
                },
                {
                    "message_id": "coreFunctions:set_commands_error_message",
                    "message": "Uhh... Something went wrong",
                },
            ],
        },
        {
            "command_id": "coreFunctions:reset_commands",
            "command_handler": "reset_commands",
            "command_description": "Deletes every command-related entry from the database",
            "command_scope": "ownerOnly",
            "messages": [
                {
                    "message_id": "coreFunctions:reset_commands_message",
                    "message": "The database is now clean! Restarting the bot to update the commands...",
                },
                {
                    "message_id": "coreFunctions:reset_commands_error_message",
                    "message": "Something went wrong :\\",
                },
            ],
        },
        {
            "command_id": "coreFunctions:restart",
            "command_handler": "restart",
            "command_description": "Restarts the bot to apply any changes",
            "command_scope": "ownerOnly",
            "messages": [
                {
                    "message_id": "coreFunctions:restarting_message",
                    "message": "Restarting...",
                },
                {
                    "message_id": "coreFunctions:restart_error_message",
                    "message": "Something went wrong while restarting :\\",
                },
            ],
        },
    ]

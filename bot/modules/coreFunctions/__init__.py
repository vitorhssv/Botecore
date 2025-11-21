from importlib import import_module
from sys import argv

# checks if the user wants to update the database or start the bot
database_update = True
if len(argv) > 1:
    if argv[1] == "-start":
        database_update = False

if not database_update:
    commands = import_module(".coreFunctions.commands", "modules")
    manage_permission_list = import_module(
        ".coreFunctions.manage_permission_list", "modules"
    )
    handlers = [
        commands.start_handler,
        commands.set_commands_handler,
        commands.reset_commands_handler,
        commands.restart_handler,
        manage_permission_list.manage_permission_list_handler,
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
        {
            "command_id": "coreFunctions:manage_permission_list",
            "command_handler": "manage_permission_list",
            "command_description": "Manages the permission list",
            "command_scope": "ownerOnly",
            "messages": [
                {
                    "message_id": "coreFunctions:add_to_list",
                    "message": "Add",
                },
                {
                    "message_id": "coreFunctions:remove_from_list",
                    "message": "Remove",
                },
                {
                    "message_id": "coreFunctions:add_or_remove_choice",
                    "message": "Do you want to add or remove contacts from the permission list?\n\nYou can /cancel this command if you want to",
                },
                {
                    "message_id": "coreFunctions:add_contact_explanation",
                    "message": "Send me the contacts you want to add!\n\nYou can /cancel this command if you want to",
                },
                {
                    "message_id": "coreFunctions:add_contacts_button",
                    "message": "Send the contacts",
                },
                {
                    "message_id": "coreFunctions:users_added_successfully",
                    "message": "All users added to the list!",
                },
                {
                    "message_id": "coreFunctions:error_while_adding_users",
                    "message": "Something went wrong while adding the users...",
                },
                {
                    "message_id": "coreFunctions:no_users_were_sent",
                    "message": "You didn't send me any users... Cancelling the command :T",
                },
                {
                    "message_id": "coreFunctions:remove_contact_explanation",
                    "message": "Alright! I'll send you a list of contacts in the bot, send me the number that identifies them separated by spaces (i.e.: 1 2 3 4 5) and I'll remove them!\n\nYou can /cancel this command if you want to",
                },
                {
                    "message_id": "coreFunctions:users_removed_from_list",
                    "message": "Done! Here's the updated list",
                },
                {
                    "message_id": "coreFunctions:error_while_removing_users",
                    "message": "Something went wrong while removing these users :/",
                },
                {
                    "message_id": "coreFunctions:allowed_list_is_empty",
                    "message": "The list is empty!",
                },
            ],
        },
        {
            "command_id": "coreFunctions:cancel",
            "command_handler": "cancel",
            "command_description": "Cancels a function",
            "command_scope": "nobody",
            "messages": [
                {
                    "message_id": "coreFunctions:cancel",
                    "message": "Command cancelled!",
                },
            ],
        },
    ]

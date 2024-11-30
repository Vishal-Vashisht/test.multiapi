from .commands import __internal_command_registration


def register_cli_commands(app):

    # Command to insert initial data in database
    __internal_command_registration(app)

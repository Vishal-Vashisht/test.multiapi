from app.api.models.models import insert_initial_data
import click


def __internal_command_registration(app):

    @app.cli.command("data-init")
    def __c1():
        insert_initial_data(app)

import click
from werkzeug.serving import run_simple
from project.web import application
from project import settings
from project.manage.database import database
from project.manage.accounts import accounts

from project.web.api import create_app
from project.core import db

app = create_app()
db.app = app


@click.group()
def cli():
    pass

cli.add_command(database)
cli.add_command(accounts)

@cli.command()
def runserver():
    "Starts the web server"
    run_simple('0.0.0.0', settings.PORT, application, use_reloader=settings.DEBUG, use_debugger=settings.DEBUG)

if __name__ == '__main__':
    cli()

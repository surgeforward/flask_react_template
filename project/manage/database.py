from ..resources.services import accounts
from ..helpers import encrypt_password
import click
from alembic import command
from alembic.config import Config

@click.group(name='db')
def database():
    pass


def _get_config():
    config = Config('alembic.ini')
    config.set_main_option('script_location', 'migrations')
    return config


@database.command()
def init():
    "Generates a new migration"
    config = _get_config()
    command.init(config, 'migrations', 'alembic')


@database.command()
def current():
    "Display the current revision for each database."
    config = _get_config()
    command.current(config)


@database.command()
@click.option('-r', '--rev-range', default=None, help="Specify a revision range; format is [start]:[end]")
def history(rev_range=None):
    "List changeset scripts in chronological order."
    config = _get_config()
    command.history(config, rev_range)


@database.command()
@click.option('--sql', default=False, help="Don't emit SQL to database - dump to standard output instead")
@click.option('--autogenerate', default=False,
              help="Populate revision script with andidate migration operatons, based on comparison of database to model")
@click.option('-m', '--message', default=None)
def revision(message=None, autogenerate=False, sql=False):
    "Create a new revision file."
    config = _get_config()
    command.revision(config, message, autogenerate=autogenerate, sql=sql)


@database.command()
@click.option('--sql', default=False, help="Don't emit SQL to database - dump to standard output instead")
@click.option('-m', '--message', default=None)
def migrate(message=None, sql=False):
    "Alias for 'revision --autogenerate'"
    config = _get_config()
    command.revision(config, message, autogenerate=True, sql=sql)


@database.command()
@click.option('--tag', default=None, help="Arbitrary 'tag' name - can be used by custom env.py scripts")
@click.option('--sql', default=False, help="Don't emit SQL to database - dump to standard output instead")
@click.option('revision', help="revision identifier")
def stamp(revision='head', sql=False, tag=None):
    "'stamp' the revision table with the given revision; don't run any migrations"
    config = _get_config()
    command.stamp(config, revision, sql=sql, tag=tag)


@database.command()
@click.option('--tag', default=None, help="Arbitrary 'tag' name - can be used by custom env.py scripts")
@click.option('--sql', default=False, help="Don't emit SQL to database - dump to standard output instead")
@click.option('--revision', default='head', help="revision identifier")
def upgrade(revision='head', sql=False, tag=None):
    "Upgrade to a later version"
    config = _get_config()
    command.upgrade(config, revision, sql=sql, tag=tag)


@database.command()
@click.option('--tag', default=None, help="Arbitrary 'tag' name - can be used by custom env.py scripts")
@click.option('--sql', default=False, help="Don't emit SQL to database - dump to standard output instead")
@click.option('revision', nargs='?', default="-1", help="revision identifier")
def downgrade(revision='-1', sql=False, tag=None):
    "Revert to a previous version"
    config = _get_config()
    command.downgrade(config, revision, sql=sql, tag=tag)


@database.command()
def branches():
    "Lists revisions that have broken the source tree into two versions representing two independent sets of changes"
    config = _get_config()
    command.branches(config)


@database.command()
def seed():
    "Seeds the database"
    seed_accounts()


def seed_accounts():
    if accounts.first(email='admin@example.com') is None:
        accounts.create(email='admin@example.com', password=encrypt_password('admin'), is_admin=True)

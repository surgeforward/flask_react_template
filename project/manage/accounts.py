import click
from werkzeug.datastructures import MultiDict

from ..resources.services import accounts as service
from ..resources.forms import RegisterForm
from ..helpers import encrypt_password

@click.group()
def accounts():
    pass


@accounts.command(name='create')
def account_create():
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    password_confirm = click.prompt('Confirm Password', hide_input=True)
    data = MultiDict(dict(email=email, password=password, password_confirm=password_confirm))
    form = RegisterForm(data, csrf_enabled=False)
    if form.validate():
        account = service.create(email=email, password=encrypt_password(password))
        print('\nUser created successfully')
        print('User(id=%s email=%s)' % (account.id, account.email))
        return
    print('\nError creating user:')
    for errors in form.errors.values():
        print('\n'.join(errors))


@accounts.command(name='delete')
def account_delete():
    email = click.prompt('Email')
    user = service.first(email=email)
    if not user:
        print('Invalid user')
        return
    service.delete(user)
    print('User deleted successfully')


@accounts.command(name='list')
def account_list():
    for u in service.all():
        print('User(id=%s email=%s)' % (u.id, u.email))
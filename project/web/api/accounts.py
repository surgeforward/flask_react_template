from flask import Blueprint
from flask_jwt import current_user
from flask.ext.bouncer import requires
from bouncer.constants import *

from ...resources.services import accounts
from ...resources.models import Account
from . import route

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@route(bp, '/current')
def whoami():
    return current_user

@route(bp, '/')
@requires(READ, Account)
def list():
    return accounts.all()

@route(bp, '/<id>')
@requires(READ, Account)
def show(id):
    return accounts.get_or_404(id)
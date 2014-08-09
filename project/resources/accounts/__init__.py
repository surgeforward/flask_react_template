from ...core import Service
from .models import Account


class AccountsService(Service):
    __model__ = Account


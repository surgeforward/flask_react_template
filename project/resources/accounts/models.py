from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer


class AccountJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'email']


class Account(AccountJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

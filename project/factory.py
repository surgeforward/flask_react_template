import os

from celery import Celery
from flask import Flask
from flask_jwt import current_user
from .core import db, mail, jwt, bouncer
from bouncer.constants import *
from .helpers import register_blueprints, check_password
from .web.middleware import HTTPMethodOverrideMiddleware
from .resources.services import accounts
import datetime


def create_app(package_name, package_path, settings_override=None, register_security_blueprint=True):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the application.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
    Blueprint should be registered. Defaults
    to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('project.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    bouncer.init_app(app)


    @jwt.authentication_handler
    def authenticate(username, password):
        account = accounts.first(email=username)
        print('here')
        if not account:
            return None

        if not check_password(password, account.password):
            return None

        return account


    @jwt.user_handler
    def load_user(payload):
        return accounts.get(payload['account_id'])


    @jwt.payload_handler
    def make_payload(account):
        exp = datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        return {
            'account_id': account.id,
            'exp': exp.strftime(app.config['JSON_DATETIME_FORMAT'])
        }

    @bouncer.authorization_method
    def define_authorization(user, they):
        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, 'Account')
            they.can(EDIT, 'Account', lambda a: a.id == user.id)

    @bouncer.user_loader
    def get_current_user():
        return current_user

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app


def create_celery_app(app=None):
    app = app or create_app('project', os.path.dirname(__file__))
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

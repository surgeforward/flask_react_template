import pkgutil
import importlib

from flask import Blueprint
from flask.json import JSONEncoder as BaseJSONEncoder
from .settings import JSON_DATETIME_FORMAT
import bcrypt


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password, pw_hash):
    return bcrypt.hashpw(password.encode('utf-8'), pw_hash.encode('utf-8')) == pw_hash


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
in all modules for the specified package.

:param app: the Flask application
:param package_name: the package name
:param package_path: the package path
"""
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
:class:`JsonSerializer` mixin.
"""
    def default(self, obj):
        if obj is None:
            return '{}'
        if hasattr(obj, 'isoformat'):
            return obj.strftime(JSON_DATETIME_FORMAT)
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerializer(object):
    """A mixin that can be used to mark a SQLAlchemy model class which
implements a :func:`to_json` method. The :func:`to_json` method is used
in conjuction with the custom :class:`JSONEncoder` class. By default this
mixin will assume all properties of the SQLAlchemy model are to be visible
in the JSON output. Extend this class to customize which properties are
public, hidden or modified before being being passed to the JSON serializer.
"""

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv
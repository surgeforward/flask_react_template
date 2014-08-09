from functools import wraps

from flask import jsonify
from flask_jwt import jwt_required

from ...core import ApplicationError, ApplicationFormError
from ...helpers import JSONEncoder
from ... import factory

def create_app(settings_override=None, register_security_blueprint=False):
    """Returns the Project API application instance"""

    app = factory.create_app(__name__, __path__, settings_override,
                             register_security_blueprint=register_security_blueprint)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers
    app.errorhandler(ApplicationError)(on_app_error)
    app.errorhandler(ApplicationFormError)(on_app_form_error)
    app.errorhandler(404)(on_404)

    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @jwt_required()
        @wraps(f)
        def wrapper(*args, **kwargs):
            status_code = 200
            return_value = f(*args, **kwargs)
            if isinstance(return_value, tuple):
                status_code = return_value[1]
                return_value = return_value[0]
            return jsonify(dict(data=return_value)), status_code
        return f

    return decorator


def on_app_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_app_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def on_404(e):
    return jsonify(dict(error='Not found')), 404


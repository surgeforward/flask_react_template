from werkzeug.wsgi import DispatcherMiddleware
from . import api, frontend

application = DispatcherMiddleware(frontend.create_app(), {
    '/api': api.create_app()
})

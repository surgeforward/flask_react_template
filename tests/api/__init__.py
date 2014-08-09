from project.web.api import create_app
from werkzeug.test import Headers, Client
from .. import ProjectAppTestCase, settings
import json

class ProjectApiTestCase(ProjectAppTestCase):

    def _create_app(self):
        return create_app(settings, register_security_blueprint=True)

    def setUp(self):
        super(ProjectApiTestCase, self).setUp()
        self.token = self._login()

    def send_get_request(self, endpoint):
        h = Headers()
        h.add('Authorization', 'Bearer {}'.format(self.token))
        return Client.open(self.client, method='GET', path=endpoint, headers=h, content_type='application/json')

    def send_post_request(self, endpoint, json_data):
        h = Headers()
        h.add('Authorization', 'Bearer {}'.format(self.token))
        return Client.open(self.client, method='POST', path=endpoint, headers=h, content_type='application/json', data=json.dumps(json_data))

    def send_put_request(self, endpoint, json_data):
        h = Headers()
        h.add('Authorization', 'Bearer {}'.format(self.token))
        return Client.open(self.client, method='PUT', path=endpoint, headers=h, content_type='application/json', data=json.dumps(json_data))

    def send_delete_request(self, endpoint):
        h = Headers()
        h.add('Authorization', 'Bearer {}'.format(self.token))
        return Client.open(self.client, method='DELETE', path=endpoint, headers=h, content_type='application/json')






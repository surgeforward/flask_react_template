from unittest import TestCase

from project.core import db
import json
from .factories import AccountFactory
from .utils import FlaskTestCaseMixin
from project.resources import services


class ProjectTestCase(TestCase):
    pass


class ProjectAppTestCase(FlaskTestCaseMixin, ProjectTestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        self.account = AccountFactory()
        services.accounts.save(self.account)

    def setUp(self):
        super(ProjectAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._create_fixtures()

    def tearDown(self):
        super(ProjectAppTestCase, self).tearDown()
        db.session.commit()
        db.drop_all()
        self.app_context.pop()

    def _login(self, username=None, password=None):
        username = username or self.account.username
        password = password or 'password'
        data = self.jpost('/auth', data={'username': username, 'password': password}, follow_redirects=False)
        return json.loads(data.data.decode())['token']

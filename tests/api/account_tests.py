from . import ProjectApiTestCase
from ..factories import AccountFactory
from project.resources import services


class AccountApiTestCase(ProjectApiTestCase):

    def test_get_current_account(self):
        r = self.send_get_request('/accounts/current')
        self.assertOkJson(r)

    def test_get_user(self):
        r = self.send_get_request('/accounts/{}'.format(self.account.id))
        self.assertOkJson(r)

    def test_get_user_not_self(self):
        new_account = AccountFactory.build()
        services.accounts.save(new_account)
        r = self.send_get_request('/accounts/{}'.format(new_account.id))
        self.assertOkJson(r)
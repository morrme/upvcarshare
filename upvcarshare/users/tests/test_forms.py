# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from test_plus import TestCase

from users.forms import SignInForm
from users.tests.factories import UserFactory
from users.tests.mocks import UPVLoginDataService

try:
    import unittest.mock as mock
except ImportError:
    import mock


@mock.patch('users.models.UPVLoginDataService', new=UPVLoginDataService)
class SigInFormTests(TestCase):
    user_factory = UserFactory

    def test_sign_in_form(self):
        user = self.make_user(username="foo")
        data = {
            "username": user.username,
            "password": "password"
        }
        form = SignInForm(data)
        self.assertTrue(form.is_valid())

    def test_sign_in_bad_password_form(self):
        user = self.make_user(username="foo")
        data = {
            "username": user.username,
            "password": "bad"
        }
        form = SignInForm(data)
        self.assertFalse(form.is_valid())

    def test_sign_in_bad_username_form(self):
        self.make_user(username="foo")
        data = {
            "username": "bad",
            "password": "password"
        }
        form = SignInForm(data)
        self.assertFalse(form.is_valid())

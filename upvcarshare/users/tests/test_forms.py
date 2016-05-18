# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from test_plus import TestCase

from users.forms import SignInForm
from users.tests.factories import UserFactory


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

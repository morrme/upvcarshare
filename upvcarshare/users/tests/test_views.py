# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from test_plus import TestCase

from users.models import User
from users.tests.factories import UserFactory


class SigInViewTests(TestCase):
    user_factory = UserFactory

    def test_get_sign_in(self):
        response = self.get("users:sign-in")
        self.response_200(response=response)

    def test_post_sign_in(self):
        user = self.make_user(username="foo")
        data = {
            "username": user.username,
            "password": "password"
        }
        response = self.post(url_name="users:sign-in", data=data)
        self.response_302(response=response)

    def test_post_bad_sign_in(self):
        user = self.make_user(username="foo")
        data = {
            "username": user.username,
            "password": "bad"
        }
        response = self.post(url_name="users:sign-in", data=data)
        self.response_200(response=response)


class EditProfileViewTests(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user(username="foo")

    def test_get_edit_profile(self):
        url_name = "users:edit"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_post_edit_profile(self):
        url_name = "users:edit"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            data = {
                "first_name": "foo",
                "last_name": "bar"
            }
            response = self.post(url_name, data=data)
            self.response_302(response=response)
            user = User.objects.get(pk=self.user.pk)
            self.assertEquals(data["first_name"], user.first_name)
            self.assertEquals(data["last_name"], user.last_name)

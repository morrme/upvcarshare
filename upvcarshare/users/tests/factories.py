# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import factory
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda n: 'foo%s' % n)
    password = make_password("password")

    class Meta:
        model = "users.User"


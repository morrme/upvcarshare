# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import factory


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda n: 'foo%s' % n)

    class Meta:
        model = "users.User"

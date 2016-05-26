# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import factory

from users.tests.factories import UserFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "notifications.Notification"

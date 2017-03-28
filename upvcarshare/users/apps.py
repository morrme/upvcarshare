# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from users.signals import create_default_groups


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        """Connects signals with their managers."""
        post_migrate.connect(create_default_groups, sender=self)

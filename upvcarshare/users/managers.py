# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.auth.models import UserManager as AuthUserManager


class UserManager(AuthUserManager):
    pass

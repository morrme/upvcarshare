# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from journeys import DEFAULT_PROJECTED_SRID


class User(AbstractUser):
    """Custom user model."""
    default_address = models.TextField(null=True, blank=True)
    default_position = models.PointField(null=True, blank=True, srid=DEFAULT_PROJECTED_SRID)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        """Override to create API Token."""
        created = self.pk is None
        result = super(User, self).save(*args, **kwargs)
        if created:
            Token.objects.create(user=self)
        return result

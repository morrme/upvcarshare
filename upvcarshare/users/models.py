# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.contrib.gis.db import models
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.templatetags.static import static
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from core.files import UploadToDir
from journeys import DEFAULT_PROJECTED_SRID, DEFAULT_DISTANCE, DEFAULT_WGS84_SRID
from users.helpers import UPVLoginDataService, from_roles_to_groups


@python_2_unicode_compatible
class User(AbstractUser):
    """Custom user model."""
    avatar = models.ImageField(
        upload_to=UploadToDir('avatars/', random_name=True),
        null=True,
        blank=True,
        max_length=255
    )

    default_address = models.TextField(
        verbose_name=_("dirección por defecto"),
        help_text=_("Dirección que por defecto se usará para crear trayectos, y que será la dirección que vean otros usuarios"),
        null=True,
        blank=True
    )

    default_distance = models.PositiveIntegerField(
        verbose_name=_("distancia por defecto"),
        help_text=_("Distancia máxima que se utilizará para encontrar trayectos (metros)"),
        null=True,
        blank=True,
        default=DEFAULT_DISTANCE
    )
    default_position = models.PointField(
        verbose_name=_("posición en el mapa por defecto"),
        null=True,
        blank=True,
        srid=DEFAULT_PROJECTED_SRID
    )

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between. In case there is no name,
        returns the username"""
        if self.first_name or self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static("img/avatar.png")

    def get_default_position_wgs84(self):
        """Transforms position to WGS-84 system."""
        if self.default_position is None:
            return None
        destination_coord = SpatialReference(DEFAULT_WGS84_SRID)
        origin_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
        trans = CoordTransform(origin_coord, destination_coord)
        position = self.default_position
        position.transform(trans)
        return position

    def set_default_position_wgs84(self, position):
        """Transforms an input to projected coordinates."""
        destination_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
        origin_coord = SpatialReference(DEFAULT_WGS84_SRID)
        trans = CoordTransform(origin_coord, destination_coord)
        position.transform(trans)
        self.default_position = position
        return self.default_position

    def update_groups(self):
        """Updates the groups using the UPV service."""
        if settings.UPV_LOGIN_IGNORE:
            return
        username = self.email.split("@")[0]
        user_data = UPVLoginDataService.user_data(username=username)
        roles = user_data.get("roles")
        groups = from_roles_to_groups(roles)
        self.groups.add(*groups)

    def save(self, *args, **kwargs):
        """Override to create API Token."""
        created = self.pk is None
        result = super(User, self).save(*args, **kwargs)
        self.update_groups()
        if created:
            Token.objects.create(user=self)
        return result

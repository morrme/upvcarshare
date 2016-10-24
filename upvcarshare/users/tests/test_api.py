# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import six
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase

from journeys import DEFAULT_PROJECTED_SRID
from users.models import User
from users.tests.factories import UserFactory


class UsersAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory(default_position=Point(882823.07, 545542.48, srid=DEFAULT_PROJECTED_SRID))

    def test_get_current_user(self):
        url = "/api/v1/users/me/"
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_current_user(self):
        url = "/api/v1/users/me/"
        self.client.force_authenticate(user=self.user)
        data = {
            "default_address": "foo",
            "default_position": {
                "type": "Point",
                "coordinates": [-0.37677, 39.46914]
            }
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=self.user.pk)
        self.assertEquals(
            "SRID=4326;POINT (-0.3767699999989411 39.46913999999702)",
            six.text_type(user.get_default_position_wgs84())
        )
        self.assertEquals("foo", user.default_address)

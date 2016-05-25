# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import json
import random

from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase

from journeys import GOING, RETURN, DEFAULT_PROJECTED_SRID
from journeys.models import Transport, Journey
from journeys.tests.factories import TransportFactory, ResidenceFactory, CampusFactory, JourneyFactory
from users.tests.factories import UserFactory


class TransportsAPITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.transports = [TransportFactory(user=self.user) for _ in range(5)]
        self.other_transport = TransportFactory(user=UserFactory())

    def test_get_transports(self):
        url = "/api/v1/transports/"
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(self.transports), len(response_data['results']))

    def test_update_transport(self):
        url = "/api/v1/transports/{}/".format(self.transports[0].pk)
        data = {
            "default_places": 2
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transport = Transport.objects.get(pk=self.transports[0].pk)
        self.assertEquals(2, transport.default_places)


class ResidenceAPITest(APITestCase):

    def test_get_residences(self):
        user = UserFactory()
        residences = [ResidenceFactory(user=user) for _ in range(5)]
        url = "/api/v1/residences/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(residences), len(response_data['results']))


class CampusAPITest(APITestCase):

    def test_get_residences(self):
        user = UserFactory()
        campus = [CampusFactory() for _ in range(5)]
        url = "/api/v1/campus/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        # Add 3 due to data migrations...
        self.assertEquals(len(campus) + 3, len(response_data['results']))


class JourneyAPITest(APITestCase):

    @staticmethod
    def _make_journey(kind=GOING):
        user = UserFactory()
        origin = ResidenceFactory(user=user)
        destination = CampusFactory()
        return JourneyFactory(user=user, residence=origin, campus=destination, kind=kind)

    def test_get_journeys(self):
        user = UserFactory()
        journeys = [self._make_journey(random.choice([GOING, RETURN])) for _ in range(5)]
        url = "/api/v1/journeys/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(journeys), len(response_data['results']))

    def test_get_journey_details(self):
        user = UserFactory()
        journey = self._make_journey(GOING)
        url = "/api/v1/journeys/{}/".format(journey.pk)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsNotNone(response_data["residence"])
        self.assertIsNotNone(response_data["campus"])

    def test_join_journey(self):
        user = UserFactory()
        journey = self._make_journey(GOING)
        url = "/api/v1/journeys/{}/join/".format(journey.pk)
        self.client.force_authenticate(user=user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(1, journey.count_passengers())

    def test_leave_journey(self):
        user = UserFactory()
        journey = self._make_journey(GOING)
        journey.join_passenger(user)
        self.assertEquals(1, journey.count_passengers())
        url = "/api/v1/journeys/{}/leave/".format(journey.pk)
        self.client.force_authenticate(user=user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(0, journey.count_passengers())

    def test_cancel_journey(self):
        user = UserFactory()
        journey = self._make_journey(GOING)
        journey.join_passenger(user)

        url = "/api/v1/journeys/{}/cancel/".format(journey.pk)
        self.client.force_authenticate(user=journey.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Journey.objects.get(pk=journey.pk).disabled)

    def test_no_cancel_journey(self):
        user = UserFactory()
        journey = self._make_journey(GOING)
        journey.join_passenger(user)

        url = "/api/v1/journeys/{}/cancel/".format(journey.pk)
        self.client.force_authenticate(user=user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Journey.objects.get(pk=journey.pk).disabled)

    def test_recommended_all_journeys(self):
        # Creates the available journeys with driver...
        user1 = UserFactory()
        residence1 = ResidenceFactory(user=user1, position=Point(883877.34, 547084.05, srid=DEFAULT_PROJECTED_SRID))
        user2 = UserFactory()
        residence2 = ResidenceFactory(user=user2, position=Point(882823.07, 545542.48, srid=DEFAULT_PROJECTED_SRID))
        campus = CampusFactory()
        user3 = UserFactory()
        residence3 = ResidenceFactory(user=user3, position=Point(865621.24, 545274.90, srid=DEFAULT_PROJECTED_SRID))
        JourneyFactory(user=user1, driver=user1, residence=residence1, campus=campus)
        JourneyFactory(user=user2, driver=user2, residence=residence2, campus=campus)
        JourneyFactory(user=user3, driver=user3, residence=residence3, campus=campus)
        user4 = UserFactory()
        residence4 = ResidenceFactory(
            user=user4, position=Point(882532.74, 545437.43, srid=DEFAULT_PROJECTED_SRID), distance=2500
        )
        JourneyFactory(user=user4, residence=residence4, campus=campus)
        # Make query...
        url = "/api/v1/journeys/recommended/"
        self.client.force_authenticate(user=user4)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(2, len(response_data['results']))

    def test_recommended_journeys(self):
        # Creates the available journeys with driver...
        user1 = UserFactory()
        residence1 = ResidenceFactory(user=user1, position=Point(883877.34, 547084.05, srid=DEFAULT_PROJECTED_SRID))
        user2 = UserFactory()
        residence2 = ResidenceFactory(user=user2, position=Point(882823.07, 545542.48, srid=DEFAULT_PROJECTED_SRID))
        campus = CampusFactory()
        user3 = UserFactory()
        residence3 = ResidenceFactory(user=user3, position=Point(865621.24, 545274.90, srid=DEFAULT_PROJECTED_SRID))
        JourneyFactory(user=user1, driver=user1, residence=residence1, campus=campus)
        JourneyFactory(user=user2, driver=user2, residence=residence2, campus=campus)
        JourneyFactory(user=user3, driver=user3, residence=residence3, campus=campus)
        user4 = UserFactory()
        residence4 = ResidenceFactory(
            user=user4, position=Point(882532.74, 545437.43, srid=DEFAULT_PROJECTED_SRID), distance=2500
        )
        journey = JourneyFactory(user=user4, residence=residence4, campus=campus)
        # Make query...
        url = "/api/v1/journeys/{}/recommended/".format(journey.pk)
        self.client.force_authenticate(user=user4)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(2, len(response_data['results']))

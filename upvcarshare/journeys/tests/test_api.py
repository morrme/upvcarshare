# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import json
import random

from rest_framework import status
from rest_framework.test import APITestCase

from journeys import GOING, RETURN
from journeys.models import Transport
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
        self.assertEquals(len(campus), len(response_data['results']))


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

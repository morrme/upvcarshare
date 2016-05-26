# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from test_plus import TestCase

from journeys import GOING
from journeys.tests.factories import CampusFactory
from journeys.tests.factories import ResidenceFactory, JourneyFactory
from notifications import JOIN, LEAVE
from notifications.models import Notification
from users.tests.factories import UserFactory


class NotificationTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    @staticmethod
    def _make_journey(user=None, kind=GOING):
        user = UserFactory() if user is None else user
        origin = ResidenceFactory(user=user)
        destination = CampusFactory()
        return JourneyFactory(user=user, residence=origin, campus=destination, kind=kind)

    def test_join_generation(self):
        user = UserFactory()
        journey = self._make_journey(self.user)
        journey.join_passenger(user)
        self.assertEquals(1, Notification.objects.filter(user=self.user, verb=JOIN).count())

    def test_leave_generation(self):
        user = UserFactory()
        journey = self._make_journey(self.user)
        journey.join_passenger(user)
        journey.leave_passenger(user)
        self.assertEquals(1, Notification.objects.filter(user=self.user, verb=JOIN).count())
        self.assertEquals(1, Notification.objects.filter(user=self.user, verb=LEAVE).count())

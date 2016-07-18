# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import datetime

from django.utils import timezone
from test_plus import TestCase

from journeys import GOING, RETURN
from journeys.models import Journey, Residence, Passenger
from journeys.tests.factories import JourneyFactory, ResidenceFactory, CampusFactory
from users.tests.factories import UserFactory


class JourneyViewTests(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user(username="foo")

    def test_get_create_journey(self):
        url_name = "journeys:create"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_post_create_journey(self):
        self.assertLoginRequired("journeys:create")
        with self.login(self.user):
            data = {
                "origin": "residence:%s" % ResidenceFactory(user=self.user).pk,
                "destiny": "campus:%s" % CampusFactory().pk,
                "free_places": 4,
                "time_window": 30,
                "departure": (timezone.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "recurrence": "",
            }
            response = self.post(url_name="journeys:create", data=data)
            self.response_302(response)
            self.assertEquals(1, Journey.objects.count())

    def test_post_create_arrival_journey(self):
        self.assertLoginRequired("journeys:create")
        with self.login(self.user):
            data = {
                "origin": "residence:%s" % ResidenceFactory(user=self.user).pk,
                "destiny": "campus:%s" % CampusFactory().pk,
                "free_places": 4,
                "time_window": 30,
                "departure": (timezone.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "arrival": (timezone.now() + datetime.timedelta(days=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "recurrence": "",
            }
            response = self.post(url_name="journeys:create", data=data)
            self.response_302(response)
            self.assertEquals(1, Journey.objects.count())

    def test_post_create_bad_arrival_journey(self):
        self.assertLoginRequired("journeys:create")
        with self.login(self.user):
            data = {
                "origin": "residence:%s" % ResidenceFactory(user=self.user).pk,
                "destiny": "campus:%s" % CampusFactory().pk,
                "free_places": 4,
                "time_window": 30,
                "departure": (timezone.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "arrival": (timezone.now() + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "recurrence": "",
            }
            response = self.post(url_name="journeys:create", data=data)
            self.response_200(response)
            self.assertEquals(0, Journey.objects.count())

    def test_post_create_bad_departure_journey(self):
        self.assertLoginRequired("journeys:create")
        with self.login(self.user):
            data = {
                "origin": "residence:%s" % ResidenceFactory(user=self.user).pk,
                "destiny": "campus:%s" % CampusFactory().pk,
                "free_places": 4,
                "time_window": 30,
                "departure": (timezone.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "arrival": (timezone.now() + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "recurrence": "",
            }
            response = self.post(url_name="journeys:create", data=data)
            self.response_200(response)
            self.assertEquals(0, Journey.objects.count())

    def test_get_edit_journey(self):
        journey = JourneyFactory(user=self.user)
        url_name = "journeys:edit"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            response = self.get(url_name, pk=journey.pk)
            self.response_200(response=response)

    def test_post_edit_journey(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        url_name = "journeys:edit"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            data = {
                "residence": ResidenceFactory(user=self.user).pk,
                "campus": CampusFactory().pk,
                "kind": RETURN,
                "free_places": 4,
                "time_window": 30,
                "departure": (timezone.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "recurrence": "",
            }
            response = self.post(url_name=url_name, pk=journey.pk, data=data)
            self.response_302(response=response)
            journey = Journey.objects.get(pk=journey.pk)
            self.assertEquals(RETURN, journey.kind)

    def test_get_recommended_journey(self):
        url_name = "journeys:recommended"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_get_recommended_journey_filter(self):
        url_name = "journeys:recommended"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name, data={"distance": 200, "kind": GOING})
            self.response_200(response=response)

    def test_get_list_journey(self):
        url_name = "journeys:list"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_post_join(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        url_name = "journeys:join"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            response = self.post(url_name=url_name, pk=journey.pk)
            self.response_302(response=response)

    def test_post_join_recurrence_all(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        journeys = [JourneyFactory(user=self.user, kind=GOING, parent=journey) for _ in range(10)]
        url_name = "journeys:join"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            data = {
                "join_to": "all"
            }
            response = self.post(url_name=url_name, pk=journey.pk, data=data)
            self.response_302(response=response)
            self.assertEquals(len(journeys) + 1, Passenger.objects.count())

    def test_post_join_recurrence_one(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        [JourneyFactory(user=self.user, kind=GOING, parent=journey) for _ in range(10)]
        url_name = "journeys:join"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            data = {
                "join_to": "one"
            }
            response = self.post(url_name=url_name, pk=journey.pk, data=data)
            self.response_302(response=response)
            self.assertEquals(1, Passenger.objects.count())

    def test_post_leave(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        journey.join_passenger(self.user)
        url_name = "journeys:leave"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            response = self.post(url_name=url_name, pk=journey.pk)
            self.response_302(response=response)

    def test_post_throw_out(self):
        journey = JourneyFactory(user=self.user, kind=GOING)
        passenger = journey.join_passenger(self.user)
        url_name = "journeys:throw-out"
        self.assertLoginRequired(url_name, pk=passenger.pk)
        with self.login(self.user):
            response = self.post(url_name=url_name, pk=passenger.pk)
            self.response_302(response=response)

    def test_cancel_journey(self):
        journey = JourneyFactory(user=self.user)
        url_name = "journeys:cancel"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            response = self.get(url_name, pk=journey.pk)
            self.response_200(response=response)

    def test_post_cancel_journey(self):
        journey = JourneyFactory(user=self.user)
        url_name = "journeys:cancel"
        self.assertLoginRequired(url_name, pk=journey.pk)
        with self.login(self.user):
            response = self.post(url_name, pk=journey.pk)
            self.response_302(response=response)
            self.assertTrue(Journey.objects.get(pk=journey.pk).disabled)

    def test_delete_journey(self):
        journeys = [JourneyFactory(user=self.user) for _ in range(10)]
        journey = JourneyFactory(user=self.user)
        url_name = "journeys:delete"
        self.assertLoginRequired(url_name, pk=journey.pk)
        self.assertEquals(len(journeys) + 1, Journey.objects.count())
        with self.login(self.user):
            response = self.get(url_name, pk=journey.pk)
            self.response_302(response=response)
            self.assertFalse(Journey.objects.filter(pk=journey.pk).exists())
            self.assertEquals(len(journeys), Journey.objects.count())

    def test_delete_parent_journeys(self):
        journey = JourneyFactory(user=self.user)
        journeys = [JourneyFactory(user=self.user, parent=journey) for _ in range(10)]
        url_name = "journeys:delete"
        self.assertLoginRequired(url_name, pk=journey.pk)
        self.assertEquals(len(journeys) + 1, Journey.objects.count())
        with self.login(self.user):
            response = self.get(url_name, pk=journey.pk)
            self.response_302(response=response)
            self.assertFalse(Journey.objects.filter(pk=journey.pk).exists())
            self.assertEquals(len(journeys), Journey.objects.count())

    def test_delete_all_journeys(self):
        journey = JourneyFactory(user=self.user)
        journeys = [JourneyFactory(user=self.user, parent=journey) for _ in range(10)]
        other_journeys = [JourneyFactory() for _ in range(5)]
        url_name = "journeys:delete-all"
        self.assertLoginRequired(url_name, pk=journey.pk)
        self.assertEquals(len(journeys) + len(other_journeys) + 1, Journey.objects.count())
        with self.login(self.user):
            response = self.get(url_name, pk=journey.pk)
            self.response_302(response=response)
            self.assertFalse(Journey.objects.filter(pk=journey.pk).exists())
            self.assertEquals(len(other_journeys), Journey.objects.count())


class ResidenceViewTests(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user(username="foo")

    def test_get_create_residence(self):
        url_name = "journeys:create-residence"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_post_create_residence(self):
        self.assertLoginRequired("journeys:create-residence")
        with self.login(self.user):
            data = {
                "name": "Home",
                "address": "foo",
                "position": "POINT (-0.3819 39.4625)",
                "distance": 500,
            }
            response = self.post(url_name="journeys:create-residence", data=data)
            self.response_302(response)
            self.assertEquals(1, Residence.objects.count())

    def test_get_edit_residence(self):
        residence = ResidenceFactory(user=self.user)
        url_name = "journeys:edit-residence"
        self.assertLoginRequired(url_name, pk=residence.pk)
        with self.login(self.user):
            response = self.get(url_name, pk=residence.pk)
            self.response_200(response=response)

    def test_post_edit_residence(self):
        residence = ResidenceFactory(user=self.user)
        url_name = "journeys:edit-residence"
        self.assertLoginRequired(url_name, pk=residence.pk)
        with self.login(self.user):
            data = {
                "name": "Home",
                "address": "bar",
                "position": "POINT (-0.3819 39.4625)",
                "distance": 500
            }
            response = self.post(url_name=url_name, pk=residence.pk, data=data)
            self.response_302(response=response)
            residence = Residence.objects.get(pk=residence.pk)
            self.assertEquals(data["address"], residence.address)

    def test_residences(self):
        ResidenceFactory(user=self.user)
        url_name = "journeys:residences"
        self.assertLoginRequired(url_name)
        with self.login(self.user):
            response = self.get(url_name)
            self.response_200(response=response)

    def test_delete_residence(self):
        residence = ResidenceFactory(user=self.user)
        url_name = "journeys:delete-residence"
        self.assertLoginRequired(url_name, pk=residence.pk)
        with self.login(self.user):
            response = self.get(url_name, pk=residence.pk)
            self.response_302(response=response)

    def test_no_delete_residence(self):
        user = UserFactory()
        residence = ResidenceFactory(user=self.user)
        url_name = "journeys:delete-residence"
        self.assertLoginRequired(url_name, pk=residence.pk)
        with self.login(user):
            response = self.get(url_name, pk=residence.pk)
            self.response_404(response=response)

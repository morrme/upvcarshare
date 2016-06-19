# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import datetime
from functools import reduce

from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.db.models import Count, F, Q
from django.utils import timezone

from journeys import GOING, RETURN
from journeys.exceptions import UserNotAllowed
from notifications import MESSAGE
from notifications.decorators import dispatch


def recommended_condition(journey, override_distance=None):
    """Creates a condition to mark a journey as recommended, based on kind and a
    needed journey.
    :param journey:
    :param override_distance:
    """
    key = "residence{}" if journey.kind == GOING else "campus{}"
    distance = getattr(journey, key.format("")).distance if override_distance is None else override_distance
    return {
        key.format("__position__distance_lte"): (
            getattr(journey, key.format("")).position,
            D(m=distance)
        ),
        "departure__lte": journey.departure + datetime.timedelta(minutes=journey.time_window),
        "departure__gte": journey.departure - datetime.timedelta(minutes=journey.time_window),
    }


class ResidenceManager(models.GeoManager):

    def smart_create(self, user):
        """Smart create using data from user.
        :param user:
        """
        return self.create(
            user=user,
            address=user.default_address,
            position=user.default_position,
            distance=user.default_distance
        )


class JourneyManager(models.GeoManager):
    """Manager for Journeys."""

    def smart_create(self, user, origin, destination, departure, transport=None):
        """Enhanced method to create journeys"""
        assert origin.__class__.__name__.lower() == "residence" or \
            origin.__class__.__name__.lower() == "campus"
        assert destination.__class__.__name__.lower() == "residence" or \
            destination.__class__.__name__.lower() == "campus"
        assert destination.__class__ != origin.__class__
        kind = GOING if origin.__class__.__name__.lower() == "residence" else RETURN
        data = {
            "user": user,
            "kind": kind,
            "departure": departure,
            origin.__class__.__name__.lower(): origin,
            destination.__class__.__name__.lower(): destination,
        }
        if transport is not None:
            data["driver"] = user
            data["free_places"] = transport.default_places
        return self.create(**data)

    def available(self, kind=None, ignore_full=False):
        """Gets all available journeys.
        :param kind: GOING, RETURN
        :param ignore_full:
        """
        now = timezone.now()
        queryset = self.filter(driver__isnull=False, departure__gt=now)
        if kind is not None:
            queryset = queryset.filter(kind=kind)
        if ignore_full:
            return queryset
        return queryset.\
            annotate(total_passengers=Count("passengers")).\
            filter(total_passengers__lt=F("free_places"))

    def nearby(self, geometry, distance, kind=None):
        """Gets available nearby journeys.
        :param distance: django.contrib.gis.measure.D
        :param geometry: django.contrib.gis.geos.GEOSGeometry
        :param kind: GOING, RETURN
        """

        nearby = self.available(kind)
        if kind is not None:
            key = "residence{}" if kind == GOING else "campus{}"
            key = key.format("__position__distance_lte")
            nearby = nearby.filter(**{key: (geometry, distance)})
        else:
            nearby = nearby.filter(
                Q(residence__position__distance_lte=(geometry, distance)) |
                Q(campus__position__distance_lte=(geometry, distance))
            )
        return nearby

    def needed(self, user, kind=None):
        """Journeys that given user needs a driver.
        :param kind:
        :param user:
        """
        now = timezone.now()
        queryset = self.filter(user=user, driver__isnull=True, departure__gt=now)
        if kind is not None:
            queryset = queryset.filter(kind=kind)
        return queryset

    def recommended(self, user, kind=None, journey=None, override_distance=None, ignore_full=False):
        """Gets the journeys recommended for an user needs.
        :param user:
        :param kind:
        :param journey:
        :param override_distance:
        :param ignore_full:
        """
        # Gets journeys needed by the user...
        if journey is None:
            needed_journeys = self.needed(user=user, kind=kind)
        else:
            needed_journeys = [journey] if not journey.is_passenger(user) else []
        # Gets conditions to search other journeys...
        conditions = [Q(**recommended_condition(journey=journey, override_distance=override_distance))
                      for journey in needed_journeys]
        if not conditions:
            return self.none()
        now = timezone.now()
        queryset = self.available(kind=kind, ignore_full=ignore_full).exclude(user=user, departure__lt=now)\
            .filter(reduce(lambda x, y: x | y, conditions))\
            .order_by("departure")
        return queryset

    def passenger(self, user):
        """Gets the journeys where the given user is passenger."""
        return self.filter(disabled=False, passengers__user=user).order_by("departure")


class MessageManager(models.Manager):
    """Manager to handle messages. """

    def list(self, user, journey=None):
        """Gets the list of all messages the given user could read.
        :param user:
        :param journey:
        """
        if journey is None:
            return self.filter(Q(journey__user=user) | Q(journey__passengers__user=user))
        if not journey.is_messenger_allowed(user):
            return self.none()
        return self.filter(journey=journey)

    @dispatch(MESSAGE)
    def send(self, user, message, journey):
        """User tries send 'message' to 'journey' group."""
        if not journey.is_messenger_allowed(user):
            raise UserNotAllowed()
        return self.create(user=user, journey=journey, content=message)

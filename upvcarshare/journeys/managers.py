# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from functools import reduce
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.db.models import Count, F, Q
from django.utils import timezone

from journeys import GOING, RETURN


def recommended_condition(journey):
    """Creates a condition to mark a journey as recommended, based on kind and a
    needed journey.
    :param kind:
    :param journey:
    """
    key = "residence{}" if journey.kind == GOING else "campus{}"
    return {
        key.format("__position__distance_lte"): (
            getattr(journey, key.format("")).position,
            D(m=getattr(journey, key.format("")).distance)
        )
    }


class ResidenceManager(models.GeoManager):

    def smart_create(self, user):
        """Smart create using data from user."""
        return self.create(
            address=user.default_address,
            position=user.default_position,
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

    def available(self, kind=None):
        """Gets all available journeys.
        :param kind: GOING, RETURN
        """
        now = timezone.now()
        queryset = self.filter(driver__isnull=False, departure__gt=now)
        if kind is not None:
            queryset = queryset.filter(kind=kind)
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

    def recommended(self, user, kind=None):
        """Gets the journeys recommended for an user needs.
        :param user:
        :param kind:
        """
        # Gets journeys needed by the user...
        needed_journeys = self.needed(user=user, kind=kind)
        conditions = [Q(**recommended_condition(journey=journey)) for journey in needed_journeys]
        return self.available(kind=kind).exclude(user=user).filter(reduce(lambda x, y: x | y, conditions))

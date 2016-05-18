# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.measure import D
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from core.models import GisTimeStampedModel
from journeys import JOURNEY_KINDS, GOING, RETURN, DEFAULT_DISTANCE, DEFAULT_PROJECTED_SRID, DEFAULT_WGS84_SRID
from journeys.exceptions import NoFreePlaces, NotAPassenger, AlreadyAPassenger
from journeys.helpers import make_point_wgs84
from journeys.managers import JourneyManager, ResidenceManager


class Place(GisTimeStampedModel):
    """Abstract class model to represent common data shared by residences and
    campus.

    Uses projected coordinate system for Spain. See: http://spatialreference.org/ref/epsg/2062/
    """
    name = models.CharField(max_length=64, blank=True, null=True)
    position = models.PointField(srid=DEFAULT_PROJECTED_SRID)
    distance = models.PositiveIntegerField(help_text=_("radius of the node on meters"))

    class Meta:
        abstract = True

    def get_position_wgs84(self):
        """Transforms position to WGS-84 system."""
        destination_coord = SpatialReference(DEFAULT_WGS84_SRID)
        origin_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
        trans = CoordTransform(origin_coord, destination_coord)
        position = self.position
        position.transform(trans)
        return position

    def set_position_wgs84(self, position):
        """Transforms an input to projected coordinates."""
        self.position = make_point_wgs84(position)
        return self.position

    def nearby(self):
        """Abstract method to search nearby journeys."""
        raise NotImplementedError()


class Residence(Place):
    """A node where life a user, and my want to go back or departure from
    here. Each residence belongs to a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="residences")
    address = models.TextField()

    objects = ResidenceManager()

    def nearby(self):
        """Search nearby journeys."""
        return Journey.objects.nearby(kind=GOING, geometry=self.position, distance=D(m=self.distance))


class Campus(Place):
    """A node that represents an university campus."""

    def nearby(self):
        """Search nearby journeys."""
        return Journey.objects.nearby(kind=RETURN, geometry=self.position, distance=D(m=self.distance))

    def save(self, **kwargs):
        if not self.distance:
            self.distance = DEFAULT_DISTANCE
        super(Campus, self).save(**kwargs)


class Journey(GisTimeStampedModel):
    """A model class to represent a journey between two node."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="journeys", help_text=_("user who creates the journey")
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, help_text=_("user who drives during the journey")
    )
    residence = models.ForeignKey("journeys.Residence", related_name="journeys")
    campus = models.ForeignKey("journeys.Campus", related_name="journeys")
    kind = models.PositiveIntegerField(choices=JOURNEY_KINDS)
    free_places = models.PositiveIntegerField(default=4)
    departure = models.DateTimeField()
    disabled = models.BooleanField(default=False)

    objects = JourneyManager()

    def origin(self):
        """Origin of the journey."""
        if self.kind == GOING:
            return self.residence
        return self.campus

    def destination(self):
        """Destination of the journey."""
        if self.kind == RETURN:
            return self.residence
        return self.campus

    def count_passengers(self):
        """Gets the count of passengers."""
        return self.passengers.count()

    def current_free_places(self):
        """Gets the current number of free places."""
        return self.free_places - self.count_passengers()

    def join_passenger(self, user):
        """A user joins a journey.
        :param user:
        """
        if self.passengers.filter(user=user).exists() or self.driver == user:
            raise AlreadyAPassenger()
        if self.count_passengers() < self.free_places:
            return Passenger.objects.create(
                journey=self,
                user=user
            )
        raise NoFreePlaces()

    def leave_passenger(self, user):
        """A user joins a journey.
        :param user:
        """
        if not self.is_passenger(user=user):
            raise NotAPassenger()
        self.passengers.filter(user=user).delete()

    def is_passenger(self, user):
        return self.passengers.filter(user=user).exists()

    def recommended(self):
        if self.driver == self.user:
            return Journey.objects.none()
        Journey.objects.recommended(user=self.user, kind=self.kind, )


class Passenger(TimeStampedModel):
    """A user who has joined a journey."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    journey = models.ForeignKey("journeys.Journey", related_name="passengers")

    class Meta:
        unique_together = ["user", "journey"]


class Transport(TimeStampedModel):
    """Saves the transport data for a user."""
    name = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transports")
    default_places = models.PositiveIntegerField(default=4)

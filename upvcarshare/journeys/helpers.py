# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import datetime
from copy import copy

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.utils import timezone

from journeys import DEFAULT_PROJECTED_SRID, DEFAULT_WGS84_SRID


def make_point(point, origin_coord_srid, destiny_coord_srid):
    origin_coord = SpatialReference(origin_coord_srid)
    destination_coord = SpatialReference(destiny_coord_srid)
    trans = CoordTransform(origin_coord, destination_coord)
    transformed_point = copy(point)
    transformed_point.transform(trans)
    return transformed_point


def make_point_wgs84(point, origin_coord_srid=DEFAULT_PROJECTED_SRID):
    """Gets a copy of the given point on WGS84 coordinates system."""
    return make_point(point, origin_coord_srid=origin_coord_srid, destiny_coord_srid=DEFAULT_WGS84_SRID)


def make_point_projected(point, origin_coord_srid=DEFAULT_WGS84_SRID):
    """Gets a copy of the given point on projected coordinates system."""
    return make_point(point, origin_coord_srid=origin_coord_srid, destiny_coord_srid=DEFAULT_PROJECTED_SRID)


def date_to_datetime(date):
    """Converts a date into time date."""
    if isinstance(date, datetime.date):
        date = datetime.datetime.combine(date, time=datetime.time(0, 0, 0, 0))
    return date


def first_day_current_week():
    """Gets the first date of the current week."""
    today = timezone.now().date()
    date = date_to_datetime(today)
    return date - datetime.timedelta(days=date.weekday())


def last_day_current_week():
    """Gets the first date of the week."""
    return first_day_current_week() + datetime.timedelta(days=7)


def expand(journey):
    """Expands given journey using recurrence field to create new journeys."""
    from journeys.models import Journey

    # Finish date is 1 of september, new course
    today = journey.departure
    finish_date = today.replace(day=1, month=9)
    if today.month >= 9:
        finish_date = finish_date.replace(year=finish_date.year + 1)
    journeys = []
    if journey.recurrence:
        datetime_start = journey.departure + datetime.timedelta(days=1)
        datetime_end = datetime.datetime.combine(finish_date, time=datetime.time(0, 0, 0, 0))
        if journey.recurrence.dtend:
            datetime_end = min(journey.recurrence.dtend, datetime_end)
        for date in journey.recurrence.occurrences(dtstart=datetime_start, dtend=datetime_end):
            new_journey = Journey.objects.get(pk=journey.pk)
            new_journey.pk = None
            new_journey.update_modified = True  # TODO I dot know why this is needed, sorry :(
            new_journey.parent = journey
            new_journey.departure = date.replace(
                hour=new_journey.departure.hour,
                minute=new_journey.departure.minute,
                tzinfo=new_journey.departure.tzinfo
            )
            if new_journey.arrival:
                new_journey.arrival = date.replace(
                    hour=new_journey.arrival.hour,
                    minute=new_journey.arrival.minute,
                    tzinfo=new_journey.arrival.tzinfo
                )
            journeys.append(new_journey)
    return journeys

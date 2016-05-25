# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import datetime
from copy import copy

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.utils import timezone

from journeys import DEFAULT_PROJECTED_SRID, DEFAULT_WGS84_SRID


def make_point_wgs84(point):
    """Gets a copy of the given point on WGS84 coordinates system."""
    origin_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
    destination_coord = SpatialReference(DEFAULT_WGS84_SRID)
    trans = CoordTransform(origin_coord, destination_coord)
    transformed_point = copy(point)
    transformed_point.transform(trans)
    return transformed_point


def make_point_projected(point, origin_coord_srid=DEFAULT_WGS84_SRID):
    """Gets a copy of the given point on projected coordinates system."""
    origin_coord = SpatialReference(origin_coord_srid)
    destination_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
    trans = CoordTransform(origin_coord, destination_coord)
    transformed_point = copy(point)
    transformed_point.transform(trans)
    return transformed_point


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

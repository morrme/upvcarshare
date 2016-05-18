# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.gis.gdal import SpatialReference, CoordTransform

from journeys import DEFAULT_PROJECTED_SRID, DEFAULT_WGS84_SRID


def make_point_wgs84(point):
    destination_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
    origin_coord = SpatialReference(DEFAULT_WGS84_SRID)
    trans = CoordTransform(origin_coord, destination_coord)
    point.transform(trans)
    return point


def make_point_projected(point):
    origin_coord = SpatialReference(DEFAULT_WGS84_SRID)
    destination_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
    trans = CoordTransform(origin_coord, destination_coord)
    point.transform(trans)
    return point

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from django.utils.translation import ugettext_lazy as _

GOING, RETURN = 0, 1
JOURNEY_KINDS = (
    (GOING, _("ida")),
    (RETURN, _("vuelta")),
)

CONFIRMED, REJECTED, UNKNOWN = 0, 1, 2
PASSENGER_STATUSES = (
    (CONFIRMED, _("Confiramado")),
    (REJECTED, _("Rechazado")),
    (UNKNOWN, _("Desconocido"))
)

# Uses projected coordinate system for Spain.
# See: https://epsg.io/2062
DEFAULT_PROJECTED_SRID = 2062
DEFAULT_WGS84_SRID = 4326
DEFAULT_GOOGLE_MAPS_SRID = 3857
# Distance in meters
DEFAULT_DISTANCE = 500
# Time window in minutes
DEFAULT_TIME_WINDOW = 30

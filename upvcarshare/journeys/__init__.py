# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from django.utils.translation import ugettext_lazy as _

GOING, RETURN = 0, 1
JOURNEY_KINDS = (
    (GOING, _("Going")),
    (RETURN, _("Return")),
)

# Uses projected coordinate system for Spain.
# See: https://epsg.io/2062
DEFAULT_PROJECTED_SRID = 2062
DEFAULT_WGS84_SRID = 4326
# Distance in meters
DEFAULT_DISTANCE = 500

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from journeys import CONFIRMED, REJECTED, UNKNOWN


def passenger_statuses(request):
    return {
        "CONFIRMED": CONFIRMED,
        "REJECTED": REJECTED,
        "UNKNOWN": UNKNOWN,
    }

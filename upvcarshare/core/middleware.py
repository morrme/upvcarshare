# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import pytz
from django.utils import timezone


class TimezoneMiddleware(object):
    """Timezone middleware to handle active time zone. By default,
    we are always in Europe/Madrid.
    """
    default_tzname = "Europe/Madrid"

    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.activate(pytz.timezone(self.default_tzname))

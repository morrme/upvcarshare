# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import pytz
from django.utils import timezone


class TimezoneMiddleware(object):
    """Timezone middleware to handle active time zone. By default,
    we are always in Europe/Madrid.
    """
    default_tzname = "Europe/Madrid"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.activate(pytz.timezone(self.default_tzname))
        response = self.get_response(request)
        return response

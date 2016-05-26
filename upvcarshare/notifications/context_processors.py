# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from notifications.models import Notification


def notifications(request):
    """Adds to the context the number or unread notifications."""
    unread_notifications = 0
    if request.user.is_authenticated():
        unread_notifications = Notification.objects.unread(user=request.user).count()
    return {
        "unread_notifications": unread_notifications,
    }

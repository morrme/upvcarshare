# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from journeys.models import Message
from notifications import MESSAGE
from notifications.models import Notification


def dispatch_message(user, journey, message):
    """Helper to dispatch creation of message from API call."""
    Notification.objects.create_from_method_call(
        verb=MESSAGE, function=Message.objects.send, args=tuple(), kwargs={
            "user": user,
            "journey": journey,
        }, result=message
    )

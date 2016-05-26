# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import SimpleLazyObject

from notifications import LEAVE, JOIN


def extract(classes, iterable):
    """Extracts objects that are instances of 'classes' from
    the given iterable.
    """
    if classes.__class__ not in (list, tuple):
        classes = (classes, )
    return list(filter(lambda item: item.__class__ in classes, iterable))


class NotificationManager(models.Manager):

    def create_from_method_call(self, verb, function, args, kwargs):
        """Creates a notification from a decorator call.
        :param verb:
        :param function:
        :param args:
        :param kwargs:
        """
        from journeys.models import Journey

        objects = list(args) + list(kwargs.values())

        # User ('actor') leaves|joins ('verb') journey ('target')
        if verb in (JOIN, LEAVE):
            notification = self.model(verb=verb)
            actor = extract([get_user_model(), SimpleLazyObject], objects)[0]
            journey = extract(Journey, objects)[0]
            notification.user = journey.user
            notification.actor = actor
            notification.target = journey
            notification.save()
            return notification

        return None

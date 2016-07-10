# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import SimpleLazyObject

from notifications import LEAVE, JOIN, CANCEL, MESSAGE, REJECT, CONFIRM, THROW_OUT


def extract(classes, iterable):
    """Extracts objects that are instances of 'classes' from
    the given iterable.
    """
    if classes.__class__ not in (list, tuple):
        classes = (classes, )
    return list(filter(lambda item: item.__class__ in classes, iterable))


class NotificationManager(models.Manager):

    def unread(self, user):
        return self.filter(user=user, read=False)

    def _create_join_leave(self, **kwargs):
        """Creates notification for a join or leave journey."""
        from journeys.models import Journey
        verb = kwargs.get("verb")
        objects = kwargs.get("objects")
        notification = self.model(verb=verb)
        actor = extract([get_user_model(), SimpleLazyObject], objects)[0]
        journey = extract(Journey, objects)[0]
        notification.user = journey.user
        notification.actor = actor
        notification.target = journey
        notification.save()
        return notification

    def _create_throw_out(self, **kwargs):
        """Creates notification for a join or leave journey."""
        from journeys.models import Journey
        verb = kwargs.get("verb")
        objects = kwargs.get("objects")
        notification = self.model(verb=verb)
        actor = extract([get_user_model(), SimpleLazyObject], objects)[0]
        journey = extract(Journey, objects)[0]
        notification.user = actor
        notification.actor = journey.user
        notification.target = journey
        notification.save()
        return notification

    def _create_confirm_reject(self, **kwargs):
        """Creates notification for a join or leave journey."""
        from journeys.models import Journey
        verb = kwargs.get("verb")
        objects = kwargs.get("objects")
        notification = self.model(verb=verb)
        actor = extract([get_user_model(), SimpleLazyObject], objects)[0]
        journey = extract(Journey, objects)[0]
        notification.user = actor
        notification.actor = journey.user
        notification.target = journey
        notification.save()
        return notification

    def _create_cancel(self, **kwargs):
        """Creates notification for a cancel journey."""
        from journeys.models import Journey
        verb = kwargs.get("verb")
        objects = kwargs.get("objects")
        notifications = []
        journey = extract(Journey, objects)[0]
        for passenger in journey.passengers.all():
            notification = self.model(verb=verb)
            notification.actor = journey
            notification.user = passenger.user
            notification.save()
            notifications.append(notification)
        return notifications

    def _create_message(self, **kwargs):
        """Creates notification for a new message."""
        from journeys.models import Journey
        verb = kwargs.get("verb")
        objects = kwargs.get("objects")
        result = kwargs.get("result")
        if result is None:
            try:
                journey = extract(Journey, objects)[0]
                actor = extract([get_user_model(), SimpleLazyObject], objects)[0]
            except KeyError:
                return None
        elif result.__class__.__name__ == "Message":
            journey = result.journey
            actor = result.user
        else:
            return None
        notifications = []
        for passenger in journey.passengers.all():
            if passenger.user != actor:
                notification = self.model(verb=verb)
                notification.actor = actor
                notification.user = passenger.user
                notification.target = journey
                notification.save()
                notifications.append(notification)
        if journey.user != actor:
            notification = self.model(verb=verb)
            notification.actor = actor
            notification.user = journey.user
            notification.target = journey
            notification.save()
            notifications.append(notification)
        return notifications

    def create_from_method_call(self, verb, function, args, kwargs, result=None):
        """Creates a notification from a decorator call.
        :param verb:
        :param function:
        :param args:
        :param kwargs:
        :param result:
        """
        # Create objects
        objects = list(args) + list(kwargs.values())
        # User ('actor') leaves|joins ('verb') journey ('target')
        if verb in (JOIN, LEAVE):
            return self._create_join_leave(verb=verb, objects=objects)
        if verb == THROW_OUT:
            return self._create_throw_out(verb=verb, objects=objects)
        elif verb in (CONFIRM, REJECT):
            return self._create_confirm_reject(verb=verb, objects=objects)
        elif verb == CANCEL:
            return self._create_cancel(verb=verb, objects=objects)
        elif verb == MESSAGE:
            return self._create_message(verb=verb, objects=objects, result=result)
        return None

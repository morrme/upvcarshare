# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from notifications.models import Notification


def dispatch(verb):
    """Creates decorator for a given verb.
    :param verb:
    :return:
    """
    def _decorator(function):
        """Decorator itself.
        :param function:
        :return:
        """
        def _wrapper_dispatch(*args, **kwargs):
            """Wrapped function with the decorator.
            :param args:
            :param kwargs:
            :return:
            """
            result = function(*args, **kwargs)
            # Creates the notification after call the function.
            Notification.objects.create_from_method_call(
                verb=verb, function=function, args=args, kwargs=kwargs, result=result
            )
            return result
        return _wrapper_dispatch
    return _decorator

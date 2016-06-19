# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import template

register = template.Library()


@register.inclusion_tag('journeys/templatetags/item.html', takes_context=True)
def journey_item(context, journey):
    """Renders a journey as an item list."""
    request = context["request"]
    context["journey_item"] = journey
    context["passenger"] = journey.passengers.filter(user=request.user).first()
    return context


@register.inclusion_tag('journeys/templatetags/join_leave_button.html', takes_context=True)
def journey_join_leave_button(context, journey):
    """Renders a journey as an item list."""
    context["journey_item"] = journey
    return context


@register.filter
def is_passenger(journey, user):
    return journey.is_passenger(user)

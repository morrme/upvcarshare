# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import template
from django.contrib.gis.geos import Point

from journeys import DEFAULT_PROJECTED_SRID, DEFAULT_GOOGLE_MAPS_SRID
from journeys.helpers import make_point

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
    request = context["request"]
    context["journey_item"] = journey
    context["passenger"] = journey.passengers.filter(user=request.user).first()
    return context


@register.filter
def is_passenger(journey, user):
    return journey.is_passenger(user)


@register.filter
def point_google_maps(origin_point):
    if isinstance(origin_point, Point) and origin_point.srid == DEFAULT_PROJECTED_SRID:
        point = make_point(
            origin_point, origin_coord_srid=DEFAULT_PROJECTED_SRID, destiny_coord_srid=DEFAULT_GOOGLE_MAPS_SRID
        )
        return "POINT ({} {})".format(point.coords[0], point.coords[1])
    return origin_point

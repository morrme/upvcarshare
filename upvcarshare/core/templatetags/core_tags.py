# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import template
from django.conf import settings
from django.http import QueryDict

from journeys import DEFAULT_GOOGLE_MAPS_SRID
from journeys.helpers import make_point

register = template.Library()


@register.simple_tag
def google_static_map(point, width=600, height=300, zoom=13):
    google_maps_point = make_point(point, origin_coord_srid=point.srid, destiny_coord_srid=DEFAULT_GOOGLE_MAPS_SRID)
    base_uri = "https://maps.googleapis.com/maps/api/staticmap"
    args = {
        "maptype": "roadmap",
        "zoom": zoom,
        "size": "{}x{}".format(width, height),
        "key": settings.GOOGLE_MAPS_API_KEY,
        "center": "{},{}".format(google_maps_point.coords[1], google_maps_point.coords[0]),
        "markers": "color:red|{},{}".format(google_maps_point.coords[1], google_maps_point.coords[0]),
    }
    query_dict = QueryDict(mutable=True)
    query_dict.update(args)
    return "{}?{}".format(base_uri, query_dict.urlencode())


@register.simple_tag(takes_context=True)
def add_active_class(context, names, _class="active"):
    request = context["request"]
    names = names.split(",")
    return _class if request.resolver_match.view_name in names else ""

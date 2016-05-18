# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from journeys.api.v1.resources import TransportResource, ResidenceResource, CampusResource, JourneyResource, \
    join_journey, leave_journey
from users.api.v1.resources import me

router = SimpleRouter()

router.register(r'transports', viewset=TransportResource)
router.register(r'residences', viewset=ResidenceResource)
router.register(r'campus', viewset=CampusResource)
router.register(r'journeys', viewset=JourneyResource)

urlpatterns = [
    url(r'^journeys/(?P<pk>[^/.]+)/join/$', join_journey, name='join-journey'),
    url(r'^journeys/(?P<pk>[^/.]+)/leave/$', leave_journey, name='leave-journey'),
    url(r'^users/me/$', me, kwargs={'pk': 'me'}),
    url(r'^', include(router.urls)),
]

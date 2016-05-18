# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url

from journeys.views import CreateJourneyView, CreateResidenceView, EditResidenceView, EditJourneyView, \
    RecommendedJourneyView, CurrentUserJourneyView

urlpatterns = [
    url(r"recommended/$", RecommendedJourneyView.as_view(), name="recommended"),
    url(r"user-list/$", CurrentUserJourneyView.as_view(), name="user-list"),
    url(r"residences/create/$", CreateResidenceView.as_view(), name="create-residence"),
    url(r"residences/(?P<pk>\d+)/edit/$", EditResidenceView.as_view(), name="edit-residence"),
    url(r"create/$", CreateJourneyView.as_view(), name="create"),
    url(r"(?P<pk>\d+)/edit/$", EditJourneyView.as_view(), name="edit"),
]

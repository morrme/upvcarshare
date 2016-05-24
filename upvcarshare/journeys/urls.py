# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url

from journeys.views import CreateJourneyView, CreateResidenceView, EditResidenceView, EditJourneyView, \
    RecommendedJourneyView, CurrentUserJourneyView, CurrentUserResidencesView, JoinJourneyView, LeaveJourneyView, \
    JourneyView, PassengerJourneyView, ThrowOutPassengerView

urlpatterns = [
    # Residences
    url(r"residences/create/$", CreateResidenceView.as_view(), name="create-residence"),
    url(r"residences/(?P<pk>\d+)/edit/$", EditResidenceView.as_view(), name="edit-residence"),
    url(r"residences/$", CurrentUserResidencesView.as_view(), name="residences"),

    # Journeys
    url(r"recommended/$", RecommendedJourneyView.as_view(), name="recommended"),
    url(r"user-list/$", CurrentUserJourneyView.as_view(), name="user-list"),
    url(r"passenger/$", PassengerJourneyView.as_view(), name="passenger"),
    url(r"create/$", CreateJourneyView.as_view(), name="create"),
    url(r"(?P<pk>\d+)/edit/$", EditJourneyView.as_view(), name="edit"),
    url(r"(?P<pk>\d+)/join/$", JoinJourneyView.as_view(), name="join"),
    url(r"(?P<pk>\d+)/leave/$", LeaveJourneyView.as_view(), name="leave"),
    url(r"(?P<pk>\d+)/throw-out/$", ThrowOutPassengerView.as_view(), name="throw-out"),
    url(r"(?P<pk>\d+)/$", JourneyView.as_view(), name="details"),

]

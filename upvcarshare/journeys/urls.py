# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url

from journeys.views.journeys import RecommendedJourneyView, JourneysView, CreateJourneyView, EditJourneyView, \
    CancelJourneyView, JoinJourneyView, LeaveJourneyView, ConfirmJourneyView, RejectJourneyView, ThrowOutPassengerView, \
    JourneyView, DeleteJourneyView
from journeys.views.places import CreateResidenceView, EditResidenceView, DeleteResidence, CurrentUserResidencesView
from journeys.views.transports import CreateTransportView, EditTransportView, DeleteTransportView, TransportListView

urlpatterns = [
    # Residences
    url(r"residences/create/$", CreateResidenceView.as_view(), name="create-residence"),
    url(r"residences/(?P<pk>\d+)/edit/$", EditResidenceView.as_view(), name="edit-residence"),
    url(r"residences/(?P<pk>\d+)/delete/$", DeleteResidence.as_view(), name="delete-residence"),
    url(r"residences/$", CurrentUserResidencesView.as_view(), name="residences"),

    # Transports
    url(r"transports/create/$", CreateTransportView.as_view(), name="create-transport"),
    url(r"transports/(?P<pk>\d+)/edit/$", EditTransportView.as_view(), name="edit-transport"),
    url(r"transports/(?P<pk>\d+)/delete/$", DeleteTransportView.as_view(), name="delete-transport"),
    url(r"transports/$", TransportListView.as_view(), name="transports"),

    # Journeys
    url(r"recommended/$", RecommendedJourneyView.as_view(), name="recommended"),
    url(r"list/$", JourneysView.as_view(), name="list"),
    url(r"create/$", CreateJourneyView.as_view(), name="create"),
    url(r"(?P<pk>\d+)/edit/$", EditJourneyView.as_view(), name="edit"),
    url(r"(?P<pk>\d+)/cancel/$", CancelJourneyView.as_view(), name="cancel"),
    url(r"(?P<pk>\d+)/delete/$", DeleteJourneyView.as_view(), name="delete"),
    url(r"(?P<pk>\d+)/join/$", JoinJourneyView.as_view(), name="join"),
    url(r"(?P<pk>\d+)/leave/$", LeaveJourneyView.as_view(), name="leave"),
    url(r"(?P<pk>\d+)/confirm/$", ConfirmJourneyView.as_view(), name="confirm"),
    url(r"(?P<pk>\d+)/reject/$", RejectJourneyView.as_view(), name="reject"),
    url(r"(?P<pk>\d+)/throw-out/$", ThrowOutPassengerView.as_view(), name="throw-out"),
    url(r"(?P<pk>\d+)/$", JourneyView.as_view(), name="details"),

]

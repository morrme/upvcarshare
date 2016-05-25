# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from journeys.api.v1.serializers import TransportSerializer, ResidenceSerializer, CampusSerializer, JourneySerializer
from journeys.models import Transport, Residence, Campus, Journey


class TransportResource(viewsets.ModelViewSet):
    """Resource to access all transports that a user has."""

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = super(TransportResource, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """On create, set the user who makes the request the owner.s"""
        serializer.save(user=self.request.user)


class ResidenceResource(viewsets.ModelViewSet):
    """Resource to access to residences. A user can create residences."""

    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """On create, set the user who makes the request the owner.s"""
        serializer.save(user=self.request.user)


class CampusResource(viewsets.ModelViewSet):
    """Resource to access all campus created on database. A user can't create a Campus."""

    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class JourneyResource(viewsets.ModelViewSet):
    """Resource to get, create or update journeys."""

    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = [
        IsAuthenticated,
    ]


class JoinJourneyResource(viewsets.ViewSet):
    """Resource to allow users to join a journey.

    Example:
    POST /api/v1/journeys/1/join/
    """
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def join(request, **kwargs):
        pk = kwargs.get('pk', 0)
        journey = get_object_or_404(Journey, pk=pk)
        journey.join_passenger(request.user)
        return Response(status=status.HTTP_201_CREATED)

join_journey = JoinJourneyResource.as_view({"post": "join"})


class LeaveJourneyResource(viewsets.ViewSet):
    """Resource to allow users to leave a journey.

    Example:
    POST /api/v1/journeys/1/leave/
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def leave(request, **kwargs):
        pk = kwargs.get('pk', 0)
        journey = get_object_or_404(Journey, pk=pk)
        journey.leave_passenger(request.user)
        return Response(status=status.HTTP_201_CREATED)

leave_journey = LeaveJourneyResource.as_view({"post": "leave"})


class RecommendedJourneysResource(viewsets.ReadOnlyModelViewSet):
    """Get recommended journeys for a given journey or for all journeys of the user.
    Eg:

    GET /api/v1/journeys/recommended/
    GET /api/v1/journeys/(id)/recommended/
    """

    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def recommended(self, request, **kwargs):
        args = {
            "user": request.user,
            "kind": request.GET.get('kind'),
        }
        pk = kwargs.get('pk', None)
        if pk is not None:
            journey = get_object_or_404(Journey, pk=pk, user=request.user)
            args["journey"] = journey
        queryset = Journey.objects.recommended(**args)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

recommended_journeys = RecommendedJourneysResource.as_view({"get": "recommended"})


class CancelJourneyResource(viewsets.ViewSet):
    """Resource to allow to cancel a journey.

    Example:
    POST /api/v1/journeys/1/cancel/
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def cancel(request, **kwargs):
        pk = kwargs.get('pk', 0)
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        journey.cancel()
        return Response(status=status.HTTP_201_CREATED)

cancel_journey = CancelJourneyResource.as_view({"post": "cancel"})


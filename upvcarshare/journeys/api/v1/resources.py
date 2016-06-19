# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from journeys.api.v1.serializers import TransportSerializer, ResidenceSerializer, CampusSerializer, JourneySerializer, \
    MessageSerializer
from journeys.exceptions import UserNotAllowed
from journeys.models import Transport, Residence, Campus, Journey, Message


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

    def get_queryset(self):
        """Only gets residences from user."""
        queryset = super(ResidenceResource, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

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

    Example:

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


class JourneyMessageResource(viewsets.ModelViewSet):
    """List the messages of a journey.

    Example:
    GET /api/v1/journeys/(id)/messages/
    """

    queryset = Message.objects.order_by("created")
    serializer_class = MessageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def messages(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is not None:
            journey = get_object_or_404(Journey, pk=pk)
        else:
            raise NotFound()
        try:
            queryset = Message.objects.list(user=request.user, journey=journey).order_by("created")
        except UserNotAllowed:
            raise PermissionDenied()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

journey_messages = JourneyMessageResource.as_view({"get": "messages"})


class MessageResource(viewsets.ModelViewSet):
    """Resource for messages."""

    queryset = Message.objects.order_by("created")
    serializer_class = MessageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        journey = self.request.query_params.get("journey")
        if journey:
            try:
                journey = Journey.objects.get(pk=journey)
                return Message.objects.list(user=self.request.user, journey=journey).order_by("created")
            except Journey.DoesNotExist:
                pass
        return Message.objects.list(user=self.request.user).order_by("created")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from notifications.api.v1.serializers import NotificationSerializer
from notifications.models import Notification


class NotificationResource(viewsets.ReadOnlyModelViewSet):

    queryset = Notification.objects.filter(read=False)
    serializer_class = NotificationSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = super(NotificationResource, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

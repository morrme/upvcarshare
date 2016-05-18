# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.api.v1.serializers import UserSerializer
from users.models import User


class UserResource(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = self.request.user.pk
        return super(UserResource, self).get_object()

me = UserResource.as_view({'get': 'retrieve', 'patch': 'partial_update'})

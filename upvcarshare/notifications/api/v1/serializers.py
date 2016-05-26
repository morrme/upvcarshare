# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from rest_framework import serializers

from journeys.api.v1.serializers import JourneySerializer
from journeys.models import Journey
from notifications.models import Notification
from users.api.v1.serializers import UserSerializer
from users.models import User


class BaseObjectRelatedField(serializers.RelatedField):
    """A custom field to use for the `actor`, `target` or `action` generic relationship."""

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        """Serialize tagged objects to a simple textual representation."""
        if isinstance(value, User):
            serializer = UserSerializer(value)
        elif isinstance(value, Journey):
            serializer = JourneySerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data


class ActorObjectRelatedField(BaseObjectRelatedField):
    pass


class TargetObjectRelatedField(BaseObjectRelatedField):
    pass


class ActionObjectRelatedField(BaseObjectRelatedField):
    pass


class NotificationSerializer(serializers.ModelSerializer):
    """Serializes a notification."""

    text = serializers.CharField()
    actor = ActionObjectRelatedField(read_only=True)
    target = TargetObjectRelatedField(read_only=True)
    action = ActionObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ["actor", "verb", "action", "target", "text", "read", "created"]

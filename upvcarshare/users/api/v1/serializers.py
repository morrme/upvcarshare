# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from journeys import DEFAULT_WGS84_SRID
from journeys.helpers import make_point_projected
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    default_position = GeometryField(source="get_default_position_wgs84")

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name", "password", "default_address",
            "default_position"
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        value = make_password(value)
        return value

    def validate(self, attrs):
        if 'get_default_position_wgs84' in attrs:
            position = attrs.pop('get_default_position_wgs84')
            position.srid = DEFAULT_WGS84_SRID
            attrs['default_position'] = make_point_projected(position)
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'get_default_position_wgs84' in validated_data:
            position = validated_data.pop('get_default_position_wgs84')
            validated_data['default_position'] = position
        return super(UserSerializer, self).update(instance, validated_data)

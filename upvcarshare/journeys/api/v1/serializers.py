# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from journeys import DEFAULT_WGS84_SRID
from journeys.helpers import make_point_projected
from journeys.models import Transport, Place, Residence, Campus, Journey
from users.api.v1.serializers import UserSerializer


class TransportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transport
        exclude = ["user"]


class PlaceSerializer(serializers.ModelSerializer):

    position = GeometryField(source="get_position_wgs84")

    class Meta:
        model = Place
        fields = ["name", "distance", "position"]

    def validate(self, attrs):
        if 'get_position_wgs84' in attrs:
            position = attrs.pop('get_position_wgs84')
            position.srid = DEFAULT_WGS84_SRID
            attrs['position'] = make_point_projected(position)
        return attrs


class ResidenceSerializer(PlaceSerializer):

    class Meta(PlaceSerializer.Meta):
        model = Residence
        fields = ["name", "distance", "position", "address"]


class CampusSerializer(PlaceSerializer):

    class Meta(PlaceSerializer.Meta):
        model = Campus


class JourneySerializer(serializers.ModelSerializer):

    user = UserSerializer()
    residence = ResidenceSerializer()
    campus = CampusSerializer()
    driver = UserSerializer()

    current_free_places = serializers.IntegerField()

    class Meta:
        model = Journey
        fields = ["user", "driver", "residence", "campus", "kind", "free_places", "departure", "disabled",
                  "current_free_places"]

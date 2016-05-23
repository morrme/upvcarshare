# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import floppyforms
from django import forms
from django.contrib.gis import admin

from core.widgets import GMapsPointWidget
from journeys.helpers import make_point_projected
from journeys.models import Residence, Journey, Campus


class PlaceAdminForm(forms.ModelForm):

    position = floppyforms.gis.PointField(widget=GMapsPointWidget(), srid=3857)

    class Meta:
        model = Residence
        fields = "__all__"

    def clean_position(self):
        position = self.cleaned_data["position"]
        position = make_point_projected(position, origin_coord_srid=3857)
        return position

    def save(self, commit=True):
        return super(PlaceAdminForm, self).save(commit=commit)


class ResidenceAdminForm(PlaceAdminForm):
    class Meta:
        model = Residence
        fields = "__all__"


class CampusAdminForm(PlaceAdminForm):
    class Meta:
        model = Campus
        fields = "__all__"


@admin.register(Residence)
class ResidenceAdminForm(admin.GeoModelAdmin):
    list_display = ["id", "user", "name", "address", "position", "created"]
    form = ResidenceAdminForm


@admin.register(Campus)
class CampusAdminForm(admin.GeoModelAdmin):
    list_display = ["id", "name", "position", "created"]
    form = CampusAdminForm


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ["id", "residence", "campus", "kind", "departure", "created"]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import floppyforms
from django import forms
from django.utils.translation import ugettext_lazy as _

from core.widgets import GMapsPointWidget
from journeys import JOURNEY_KINDS
from journeys.helpers import make_point_projected
from journeys.models import Residence, Journey
from users.models import User


class ResidenceForm(forms.ModelForm):
    """Form to edit and create residences. It uses a OpenStreetMap widget that
    uses a SRID 3857, so we have to convert all input data from this widget to
    our projected coordinates system.
    """

    position = floppyforms.gis.PointField(label=_("Posición en el mapa"), widget=GMapsPointWidget(), srid=3857)

    class Meta:
        model = Residence
        fields = ["name", "address", "position", "distance"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control"}),
            "distance": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_position(self):
        position = self.cleaned_data["position"]
        position = make_point_projected(position, origin_coord_srid=3857)
        return position

    def save(self, commit=True, **kwargs):
        """When save a residence form, you have to provide an user."""
        assert "user" in kwargs
        assert isinstance(kwargs["user"], User)
        residence = super(ResidenceForm, self).save(commit=False)
        residence.user = kwargs.get("user")
        if commit:
            residence.save()
        return residence


class JourneyForm(forms.ModelForm):

    i_am_driver = forms.BooleanField(label=_("¿Soy conductor?"), required=False)

    class Meta:
        model = Journey
        fields = ["residence", "campus", "kind", "i_am_driver", "free_places", "departure", "time_window"]
        widgets = {
            "residence": forms.Select(attrs={"class": "form-control"}),
            "campus": forms.Select(attrs={"class": "form-control"}),
            "kind": forms.Select(attrs={"class": "form-control"}),
            "free_places": forms.NumberInput(attrs={"class": "form-control"}),
            "departure": floppyforms.DateTimeInput(attrs={"class": "form-control"}),
            "time_window": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(JourneyForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['residence'].queryset = Residence.objects.filter(user=self.user)

    def save(self, commit=True, **kwargs):
        """When save a journey form, you have to provide an user."""
        user = self.user
        if "user" in kwargs:
            assert isinstance(kwargs["user"], User)
            user = kwargs.get("user")
        journey = super(JourneyForm, self).save(commit=False)
        journey.user = user
        journey.driver = user if self.cleaned_data["i_am_driver"] else None
        if commit:
            journey.save()
        return journey


class FilterForm(forms.Form):
    """Form to filter search results."""

    kind = forms.IntegerField(
        label=_("Tipo de viaje"),
        required=False,
        widget=forms.Select(
            attrs={"class": "form-control"},
            choices=JOURNEY_KINDS
        )
    )
    distance = forms.IntegerField(
        label=_("Distancia (metros)"),
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control"},
        ),
    )


class CancelJourneyForm(forms.Form):
    """Form to handle the cancellation of a journey. A cancellation needs a
    confirmation of the user.
    """
    pass


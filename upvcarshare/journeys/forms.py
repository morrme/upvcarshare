# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import floppyforms
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from core.widgets import GMapsPointWidget
from journeys import JOURNEY_KINDS, GOING, RETURN
from journeys.helpers import make_point_projected
from journeys.models import Residence, Journey, Campus, Transport
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

    i_am_driver = forms.BooleanField(
        label=_("¿Eres conductor?"),
        required=False,
        initial=False,
        widget=forms.RadioSelect(
            choices=((True, _('Sí')), (False, _('No'))),
        )
    )

    class Meta:
        model = Journey
        fields = ["residence", "campus", "kind", "i_am_driver", "transport", "free_places", "departure", "time_window",
                  "recurrence"]
        widgets = {
            "transport": forms.Select(attrs={"class": "form-control"}),
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
            self.fields['transport'].queryset = Transport.objects.filter(user=self.user)

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


class SmartJourneyForm(forms.ModelForm):

    origin = forms.CharField(widget=forms.HiddenInput())
    destiny = forms.CharField(widget=forms.HiddenInput())

    i_am_driver = forms.BooleanField(
        label=_("¿Soy conductor?"),
        required=False,
        initial=False,
        widget=forms.RadioSelect(
            choices=((True, _('Sí')), (False, _('No'))),
        )
    )

    class Meta:
        model = Journey
        fields = ["origin", "destiny", "i_am_driver", "transport", "free_places", "departure", "time_window",
                  "recurrence"]
        widgets = {
            "transport": forms.Select(attrs={"class": "form-control"}),
            "kind": forms.Select(attrs={"class": "form-control"}),
            "free_places": forms.NumberInput(attrs={"class": "form-control"}),
            "departure": floppyforms.DateTimeInput(attrs={"class": "form-control"}),
            "time_window": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SmartJourneyForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['transport'].queryset = Transport.objects.filter(user=self.user)

    def clean_origin(self):
        origin = self.cleaned_data["origin"]
        data = origin.split(":")
        models = {"residence": Residence, "campus": Campus}
        try:
            return models.get(data[0]).objects.get(pk=data[1])
        except (ObjectDoesNotExist, IndexError, AttributeError):
            raise forms.ValidationError(_("Lugar de origen no válido"))

    def clean_destiny(self):
        destiny = self.cleaned_data["destiny"]
        data = destiny.split(":")
        models = {"residence": Residence, "campus": Campus}
        try:
            return models.get(data[0]).objects.get(pk=data[1])
        except (ObjectDoesNotExist, IndexError, AttributeError):
            raise forms.ValidationError(_("Lugar de destino no válido"))

    def save(self, commit=True, **kwargs):
        """When save a journey form, you have to provide an user."""
        user = self.user
        if "user" in kwargs:
            assert isinstance(kwargs["user"], User)
            user = kwargs.get("user")
        journey = super(SmartJourneyForm, self).save(commit=False)
        journey.user = user
        journey.driver = user if self.cleaned_data["i_am_driver"] else None
        # Smart origin, destiny and kind
        origin = self.cleaned_data["origin"]
        destiny = self.cleaned_data["destiny"]
        attribute_selector = {
            Residence: "residence",
            Campus: "campus",
        }
        attribute = attribute_selector[origin.__class__]
        setattr(journey, attribute, origin)
        attribute = attribute_selector[destiny.__class__]
        setattr(journey, attribute, destiny)
        journey.kind = GOING if isinstance(origin, Residence) else RETURN
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


class ConfirmRejectJourneyForm(forms.Form):
    """Form to get the user to confirm or reject."""

    user = forms.IntegerField(widget=forms.HiddenInput())

    def clean_user(self):
        user_pk = self.cleaned_data["user"]
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise forms.ValidationError(_("El usuario no existe"))
        return user


class TransportForm(forms.ModelForm):
    """Form to create transport data."""

    class Meta:
        model = Transport
        fields = ["name", "default_places", "brand", "model", "color"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "default_places": forms.NumberInput(attrs={"class": "form-control"}),
            "brand": floppyforms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(TransportForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, **kwargs):
        """When save a transport form, you have to provide an user."""
        user = self.user
        if "user" in kwargs:
            assert isinstance(kwargs["user"], User)
            user = kwargs.get("user")
        transport = super(TransportForm, self).save(commit=False)
        transport.user = user
        if commit:
            transport.save()
        return transport

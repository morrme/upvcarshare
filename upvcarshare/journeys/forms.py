# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import forms

from journeys.models import Residence, Journey
from users.models import User


class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        fields = ["name", "address", "position", "distance"]

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

    class Meta:
        model = Journey
        fields = ["residence", "campus", "kind", "free_places", "departure", "disabled"]

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
        if commit:
            journey.save()
        return journey

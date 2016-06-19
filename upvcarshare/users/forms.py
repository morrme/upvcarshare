# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import floppyforms
from django import forms
from django.utils.translation import ugettext_lazy as _

from core.widgets import GMapsPointWidget
from journeys.helpers import make_point_projected
from users.models import User


class SignInForm(forms.Form):
    """Form for handle in a user can log in."""

    username = forms.fields.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Nombre de usuario"),
            "autocapitalize": "off",
            "autocorrect": "off",
            "autofocus": "autofocus",
        }),
        error_messages={'required': _('El nombre de usuario es obligatorio')}
    )
    password = forms.fields.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Contraseña")
        }),
        error_messages={'required': _('La contraseña es obligatoria')}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Nombre de usuario no encontrado"))
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError(_("La contraseña no es correcta"))
        except User.DoesNotExist:
            pass
        return password


class UserForm(forms.ModelForm):
    """Form to edit information of the user."""

    default_position = floppyforms.gis.PointField(
        label=_("Posicion por defecto"),
        widget=GMapsPointWidget(),
        srid=3857,
        required=False
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "avatar", "default_address", "default_position", "default_distance"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "default_address": forms.Textarea(attrs={"class": "form-control"}),
            "default_distance": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_default_position(self):
        default_position = self.cleaned_data["default_position"]
        if default_position:
            default_position = make_point_projected(default_position, origin_coord_srid=3857)
        return default_position

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from users.models import User


class SignInForm(forms.Form):
    """Form for handle in a user can log in."""
    username = forms.fields.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Username"),
            "autocapitalize": "off",
            "autocorrect": "off",
            "autofocus": "autofocus",
        }),
        error_messages={'required': _('The username is required')}
    )
    password = forms.fields.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Password")
        }),
        error_messages={'required': _('The password is required')}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Username not found"))
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError(_("Password incorrect"))
        except User.DoesNotExist:
            pass
        return password


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "default_address", "default_position", "default_distance"]

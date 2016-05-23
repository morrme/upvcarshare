# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url

from users.views import SignInView, EditProfileView, SignOutView

urlpatterns = [
    url(r"sign-out/$", SignOutView.as_view(), name="sign-out"),
    url(r"sign-in/$", SignInView.as_view(), name="sign-in"),
    url(r"edit/$", EditProfileView.as_view(), name="edit"),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url

from notifications.views import NotificationListView, ReadNotificationsView

urlpatterns = [
    url(r"read/$", ReadNotificationsView.as_view(), name="read"),
    url(r"$", NotificationListView.as_view(), name="list"),
]

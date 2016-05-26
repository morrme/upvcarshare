# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from braces.views import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View

from notifications.models import Notification


class NotificationListView(LoginRequiredMixin, View):
    """View to list all the notifications of the user."""
    template_name = "notifications/list.html"

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        data = {
            "notifications": notifications
        }
        return render(request, self.template_name, data)


class ReadNotificationsView(LoginRequiredMixin, View):
    """Sets all notifications as read."""

    @staticmethod
    def post(request):
        notifications = Notification.objects.filter(user=request.user, read=False)
        notifications.update(read=True)
        return redirect("notifications:list")


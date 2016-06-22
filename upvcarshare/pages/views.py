# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View


class HomeView(View):
    """Home view to redirect to recommended journeys."""

    @staticmethod
    def get(request):
        return redirect(reverse("journeys:recommended"))

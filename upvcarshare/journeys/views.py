# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from braces.views import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from journeys.forms import JourneyForm, ResidenceForm
from journeys.models import Journey, Residence


class CreateResidenceView(LoginRequiredMixin, View):
    """View to show journey creation form and to handle its creation."""

    template_name = "residences/create.html"

    def get(self, request):
        form = ResidenceForm()
        data = {
            "form": form
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = ResidenceForm(request.POST)
        data = {
            "form": form
        }
        if form.is_valid():
            journey = form.save(user=request.user)
            data["journey"] = journey
        return render(request, self.template_name, data)


class EditResidenceView(LoginRequiredMixin, View):
    """View to edit residences."""

    template_name = "residences/edit.html"

    def get(self, request, pk):
        residence = get_object_or_404(Residence, pk=pk, user=request.user)
        form = ResidenceForm(instance=residence)
        data = {
            "form": form,
            "residence": residence,
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        residence = get_object_or_404(Residence, pk=pk, user=request.user)
        form = ResidenceForm(request.POST, instance=residence)
        data = {
            "form": form,
            "residence": residence,
        }
        if form.is_valid():
            form.save(user=request.user)
        return render(request, self.template_name, data)


class CreateJourneyView(LoginRequiredMixin, View):
    """View to show journey creation form and to handle its creation."""

    template_name = "journeys/create.html"

    def get(self, request):
        form = JourneyForm(user=request.user)
        data = {
            "form": form
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = JourneyForm(request.POST, user=request.user)
        data = {
            "form": form
        }
        if form.is_valid():
            journey = form.save()
            data["journey"] = journey
        return render(request, self.template_name, data)


class EditJourneyView(LoginRequiredMixin, View):
    """View to edit journeys."""

    template_name = "journeys/edit.html"

    def get(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        form = JourneyForm(instance=journey, user=request.user)
        data = {
            "form": form,
            "journey": journey,
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        form = JourneyForm(request.POST, instance=journey, user=request.user)
        data = {
            "form": form,
            "journey": journey,
        }
        if form.is_valid():
            form.save()
        return render(request, self.template_name, data)


class RecommendedJourneyView(LoginRequiredMixin, View):
    """View to show to the user the list of recommended journeys according to his needs."""
    template_name = "journeys/recommended.html"

    def get(self, request):
        kind_filter = request.GET.get("kind")
        data = {
            "journeys": Journey.objects.recommended(user=request.user, kind=kind_filter)
        }
        return render(request, self.template_name, data)


class CurrentUserJourneyView(LoginRequiredMixin, View):
    """View to show to the user the list of his created journeys."""
    template_name = "journeys/user_list.html"

    def get(self, request):
        data = {
            "journeys": Journey.objects.filter(user=request.user)
        }
        return render(request, self.template_name, data)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import datetime
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _

from journeys import GOING
from journeys.exceptions import AlreadyAPassenger, NoFreePlaces, NotAPassenger
from journeys.forms import SmartJourneyForm, JourneyForm, FilterForm, ConfirmRejectJourneyForm, SearchJourneyForm
from journeys.models import Residence, Campus, Journey, Passenger


class CreateJourneyView(LoginRequiredMixin, View):
    """View to show journey creation form and to handle its creation."""

    template_name = "journeys/create.smart.html"
    form = SmartJourneyForm

    def get(self, request):
        residences = Residence.objects.filter(user=request.user)
        campuses = Campus.objects.all()
        initial_departure = timezone.now().replace(second=0, minute=0) + datetime.timedelta(hours=1)
        initial = {
            "residence": residences.first() if residences.exists() else None,
            "campus": campuses.first() if campuses.exists() else None,
            "kind": GOING,
            "departure": initial_departure,
            "arrival": initial_departure + datetime.timedelta(minutes=30)
        }
        form = self.form(initial=initial, user=request.user)
        data = {
            "form": form
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form(request.POST, user=request.user)
        data = {
            "form": form
        }
        if form.is_valid():
            journey = form.save()
            return redirect("journeys:details", pk=journey.pk)
        return render(request, self.template_name, data)


class EditJourneyView(LoginRequiredMixin, View):
    """View to edit journeys."""

    template_name = "journeys/edit.html"

    def get(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        form = JourneyForm(
            instance=journey,
            initial={"i_am_driver": journey.driver is not None and journey.driver == request.user},
            user=request.user
        )
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
            return redirect("journeys:details", pk=journey.pk)
        return render(request, self.template_name, data)


class JourneyView(LoginRequiredMixin, View):
    """View to journey details."""

    template_name = "journeys/details.html"

    @staticmethod
    def show_passengers(request, journey):
        if journey.user == request.user:
            return True
        return journey.is_passenger(request.user) and journey.count_passengers() > 0 and not journey.needs_driver()

    @staticmethod
    def show_messenger(request, journey):
        if journey.user == request.user and not journey.needs_driver():
            return True
        return journey.is_passenger(request.user)

    def get(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk)
        data = {
            "journey": journey,
            "show_passengers": self.show_passengers(request, journey),
            "show_messenger": self.show_messenger(request, journey),
            "is_fulfilled": journey.is_fulfilled(),
            "fulfilled_by": journey.fulfilled_by(),
            "passengers": journey.passengers_list(request.user),
            "recommended": journey.recommended(),
            "has_recurrence": journey.parent is not None or journey.children.exists()
        }
        return render(request, self.template_name, data)


class RecommendedJourneyView(LoginRequiredMixin, View):
    """View to show to the user the list of recommended journeys according to his needs."""
    template_name = "journeys/recommended.html"

    def get(self, request):
        filter_form = FilterForm(request.GET)
        kind_filter = None
        override_distance = None
        if filter_form.is_valid():
            kind_filter = filter_form.cleaned_data.get("kind")
            override_distance = filter_form.cleaned_data.get("distance")
        data = {
            "filter_form": filter_form,
            "journeys": Journey.objects.recommended(
                user=request.user,
                kind=kind_filter,
                override_distance=override_distance
            ),
        }
        return render(request, self.template_name, data)


class JourneysView(LoginRequiredMixin, View):
    """View to show to the user the list of his created journeys."""
    template_name = "journeys/list.html"

    def get(self, request):
        journeys = Journey.objects.filter(user=request.user).order_by("departure")
        data = {
            "journeys": journeys,
            "journeys_count": journeys.count()
        }
        return render(request, self.template_name, data)


class JoinJourneyView(LoginRequiredMixin, View):
    """View to handle the action of joining a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk)
        join_to = request.POST.get("join_to")
        try:
            journey.join_passenger(request.user, join_to)
            if join_to == "all":
                messages.success(request, _('Has solicitado unirte a todos los viajes disponibles'))
            else:
                messages.success(request, _('Has solicitado unirte al viaje'))
        except AlreadyAPassenger:
            messages.error(request, _('¡Ya has solicitado unirte al viaje!'))
        except NoFreePlaces:
            messages.error(request, _('No quedan plazas libres en el viaje'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class ConfirmJourneyView(LoginRequiredMixin, View):
    """View to handle the action of joining a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        passenger = get_object_or_404(Passenger, pk=pk)
        if passenger.journey.user != request.user:
            raise Http404
        form = ConfirmRejectJourneyForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            try:
                passenger.journey.confirm_passenger(user)
            except NotAPassenger:
                messages.success(request, _('El usuario no está en este viaje'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class RejectJourneyView(LoginRequiredMixin, View):
    """View to handle the action of joining a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        passenger = get_object_or_404(Passenger, pk=pk)
        if passenger.journey.user != request.user:
            raise Http404
        form = ConfirmRejectJourneyForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            try:
                passenger.journey.reject_passenger(user)
            except NotAPassenger:
                messages.success(request, _('El usuario no está en este viaje'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class LeaveJourneyView(LoginRequiredMixin, View):
    """View to handle the action of leaving a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk)
        try:
            journey.leave_passenger(request.user)
            messages.success(request, _('Has dejado el viaje'))
        except NotAPassenger:
            messages.success(request, _('No estás en este viaje'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class ThrowOutPassengerView(LoginRequiredMixin, View):
    """View to handle the action of throw out a passenger. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        passenger = get_object_or_404(Passenger, pk=pk)
        if passenger.journey.user != request.user:
            raise Http404
        try:
            passenger.journey.throw_out(passenger.user)
            messages.success(request, _('Has expulsado al pasajero'))
        except NotAPassenger:
            messages.success(request, _('No puedes expulsar a este pasajero'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class AcceptPassengerView(LoginRequiredMixin, View):
    """View to accept a request of a possible passenger."""
    return_to = "journeys:recommended"

    def post(self, request, pk):

        passenger = get_object_or_404(Passenger, pk=pk)
        if passenger.journey.user != request.user:
            raise Http404
        try:
            passenger.journey.leave_passenger(passenger.user)
            messages.success(request, _('Has expulsado al pasajero'))
        except NotAPassenger:
            messages.success(request, _('No puedes expulsar a este pasajero'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class CancelJourneyView(LoginRequiredMixin, View):
    """View to handle a cancellation of a journey."""
    template_name = "journeys/cancel.html"

    def get(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        data = {
            "journey": journey,
        }
        return render(request, self.template_name, data)

    @staticmethod
    def post(request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        journey.cancel()
        return redirect("journeys:details", pk=journey.pk)


class DeleteJourneyView(LoginRequiredMixin, View):
    """Deletes a journey only if it hasn't driver."""

    @staticmethod
    def get(request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        # Delete only if the journey hasn't driver
        if journey.driver is None:
            if journey.has_recurrence and journey.children.exists():
                new_parent = journey.children.order_by("departure").first()
                journey.children.exclude(pk=new_parent.pk).update(parent=new_parent)
                new_parent.parent = None
                new_parent.save()
                # Get again the journey
                journey = get_object_or_404(Journey, pk=pk, user=request.user)
            journey.delete()
            messages.success(request, _('Has borrado el viaje'))
            return redirect("journeys:list")
        messages.error(request, _('No puedes borrar este viaje'))
        return redirect(reverse("journeys:details", kwargs={"pk": pk}))


class DeleteAllJourneyView(LoginRequiredMixin, View):
    """Deletes a journey only if it hasn't driver."""

    @staticmethod
    def get(request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        # Delete only if the journey hasn't driver
        if journey.driver is None:
            if journey.has_recurrence:
                if journey.parent is not None:
                    journeys = journey.parent.children.filter(departure__gte=journey.departure)
                    journeys.delete()
                else:
                    journey.delete()
            else:
                journey.delete()
            messages.success(request, _('Has borrado el viaje y sus repeticiones'))
            return redirect("journeys:list")
        messages.error(request, _('No puedes borrar este viaje'))
        return redirect(reverse("journeys:details", kwargs={"pk": pk}))

class SearchJourneysView(LoginRequiredMixin, View):
    """View to search journeys."""
    template_name = "journeys/search.html"

    def get(self, request):
        journeys = Journey.objects.none()
        is_query = bool(request.GET)
        if is_query:
            form = SearchJourneyForm(request.GET)
            if form.is_valid():
                journeys = form.search(user=request.user)
        else:
            form = SearchJourneyForm(initial={"time_window": 30})
        data = {
            "form": form,
            "journeys": journeys,
            "is_query": is_query
        }
        return render(request, self.template_name, data)

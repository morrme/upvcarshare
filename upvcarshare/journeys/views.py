# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from journeys import GOING
from journeys.exceptions import AlreadyAPassenger, NoFreePlaces, NotAPassenger
from journeys.forms import JourneyForm, ResidenceForm, FilterForm, CancelJourneyForm, SmartJourneyForm, \
    ConfirmRejectJourneyForm, TransportForm
from journeys.models import Journey, Residence, Campus, Passenger, Transport


class CreateResidenceView(LoginRequiredMixin, View):
    """View to show journey creation form and to handle its creation."""

    template_name = "residences/create.html"

    def get(self, request):
        initial = {
            "address": request.user.default_address,
            "position": request.user.default_position,
            "distance": request.user.default_distance,
        }
        form = ResidenceForm(initial=initial)
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
            residence = form.save(user=request.user)
            return redirect("journeys:edit-residence", pk=residence.pk)
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

    template_name = "journeys/create.smart.html"
    form = SmartJourneyForm

    def get(self, request):
        residences = Residence.objects.filter(user=request.user)
        campuses = Campus.objects.all()
        initial = {
            "residence": residences.first() if residences.exists() else None,
            "campus": campuses.first() if campuses.exists() else None,
            "kind": GOING,
            "departure": timezone.now().replace(second=0)
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


class CurrentUserJourneyView(LoginRequiredMixin, View):
    """View to show to the user the list of his created journeys."""
    template_name = "journeys/user_list.html"

    def get(self, request):
        now = timezone.now()
        data = {
            "journeys": Journey.objects.filter(
                user=request.user,
                departure__gte=now
            ).order_by("departure")
        }
        return render(request, self.template_name, data)


class CurrentUserResidencesView(LoginRequiredMixin, View):
    """View to show to the user the list of his created residences."""

    template_name = "residences/list.html"

    def get(self, request):
        data = {
            "residences": Residence.objects.filter(user=request.user)
        }
        return render(request, self.template_name, data)


class PassengerJourneyView(LoginRequiredMixin, View):
    """View to show the list of journeys where the user is passenger."""
    template_name = "journeys/passenger.html"

    def get(self, request):
        data = {
            "journeys": Journey.objects.passenger(user=request.user)
        }
        return render(request, self.template_name, data)


class JoinJourneyView(LoginRequiredMixin, View):
    """View to handle the action of joining a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk)
        try:
            journey.join_passenger(request.user)
            messages.success(request, _('Has solicitado unirte al trayecto'))
        except AlreadyAPassenger:
            messages.error(request, _('¡Ya has solicitado unirte al trayecto!'))
        except NoFreePlaces:
            messages.error(request, _('No quedan plazas libres en el trayecto'))
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
                messages.success(request, _('El usuario no está en este trayecto'))
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
                messages.success(request, _('El usuario no está en este trayecto'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class LeaveJourneyView(LoginRequiredMixin, View):
    """View to handle the action of leaving a journey. """
    return_to = "journeys:recommended"

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk)
        try:
            journey.leave_passenger(request.user)
            messages.success(request, _('Has dejado el trayecto'))
        except NotAPassenger:
            messages.success(request, _('No estás en este trayecto'))
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
            passenger.journey.leave_passenger(passenger.user)
            messages.success(request, _('Has expulsado al pasajero'))
        except NotAPassenger:
            messages.success(request, _('No puedes expulsar a este pasajero'))
        return_to = request.POST.get("return_to", self.return_to)
        return redirect(return_to)


class AcceptPassengerView(LoginRequiredMixin, View):
    """View to accept a request of a possible passenger."""
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


class DeleteResidence(LoginRequiredMixin, View):
    """Deletes a residence if there is no journeys related."""

    def get(self, request, pk):
        residence = get_object_or_404(Residence, pk=pk, user=request.user)
        if residence.journeys.count() == 0:
            residence.delete()
            messages.success(request, _('Has borrado el lugar'))
            return redirect("journeys:residences")
        messages.error(request, _('No puedes borrar este lugar'))
        return redirect("journeys:residences")


class CancelJourneyView(LoginRequiredMixin, View):
    """View to handle a cancellation of a journey."""
    template_name = "journeys/cancel.html"

    def get(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        data = {
            "journey": journey,
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        journey = get_object_or_404(Journey, pk=pk, user=request.user)
        journey.cancel()
        return redirect("journeys:details", pk=journey.pk)


class TransportListView(LoginRequiredMixin, View):
    """Shows the list of users' transports."""
    template_name = "transports/list.html"

    def get(self, request):
        data = {
            "transports": Transport.objects.filter(user=request.user)
        }
        return render(request, self.template_name, data)


class CreateTransportView(LoginRequiredMixin, View):
    """Handles the creation of a new transport."""
    template_name = "transports/create.html"
    form = TransportForm

    def get(self, request):
        data = {
            "form": self.form(user=request.user)
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form(request.POST, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, _('Has creado el transporte correctamente'))
            return redirect("journeys:transports")
        data = {"form": form}
        return render(request, self.template_name, data)


class EditTransportView(LoginRequiredMixin, View):
    """Handles the edition of a new transport."""
    template_name = "transports/edit.html"
    form = TransportForm

    def get(self, request, pk):
        transport = get_object_or_404(Transport, pk=pk, user=request.user)
        data = {
            "form": self.form(instance=transport, user=request.user),
            "transport": transport
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        transport = get_object_or_404(Transport, pk=pk, user=request.user)
        form = self.form(request.POST, user=request.user, instance=transport)
        if form.is_valid():
            messages.success(request, _('Has editado el transporte correctamente'))
            return redirect("journeys:transports")
        data = {
            "form": form,
            "transport": transport
        }
        return render(request, self.template_name, data)


class DeleteTransportView(LoginRequiredMixin, View):
    pass

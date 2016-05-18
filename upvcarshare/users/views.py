# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from braces.views import CsrfExemptMixin
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View

from users.forms import SignInForm, UserForm


class SignInView(CsrfExemptMixin, View):
    """View to allow  to login users into the platform."""
    template_name = "users/sign_in.html"

    @staticmethod
    def get_next_page(request):
        """Gets the page to go after log in."""
        default_redirect = reverse('home')
        next_page = request.GET.get('next') or request.POST.get('next')
        return next_page or default_redirect

    def get(self, request):
        data = {
            "form": SignInForm(),
            "next": request.GET.get('next')
        }
        return render(request, self.template_name, data)

    def post(self, request):
        next_page = self.get_next_page(request=request)
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
                request=request
            )
            if user is not None:
                login(request, user)
                return redirect(next_page)
        data = {"form": form, "next": next_page}
        return render(request, self.template_name, data)


class EditProfileView(LoginRequiredMixin, View):
    """View to edit profile of the current user."""

    template_name = "users/edit.html"

    def get(self, request):
        form = UserForm(instance=request.user)
        data = {
            "form": form
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = UserForm(request.POST, instance=request.user)
        data = {
            "form": form
        }
        print(form.errors)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, data)


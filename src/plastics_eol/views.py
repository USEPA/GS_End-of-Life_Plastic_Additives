# views.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import ConditionForm, ScenarioForm
from .models import Condition, ExportedPlastic, ImportedPlastic, \
    ReExportedPlastic, MSWComposition, MSWCompost, MSWIncineration, \
    MSWLandfill, MSWRecycling, PlasticIncineration, PlasticLandfill, \
    PlasticRecycling, PlasticReportedRecycled, Scenario
from .utils import get_steps


def home(request):
    """Render the home page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'index.html', {
        'title': 'Home Page',
    })


def contact(request):
    """Render the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 'main/contact.html', {
            'title': 'Contact',
            'message': 'Your contact page.',
        })


def about(request):
    """Render the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 'main/about.html', {
            'title': 'About',
            'message': 'Your application description page.',
        })


class ScenarioList(LoginRequiredMixin, ListView):
    """
    Scenario Index View where a user can view existing, edit existing,
    delete existing, and create new calculator scenarios.
    """

    model = Scenario
    template_name = 'scenario/scenario_list.html'
    context_object_name = 'scenario_list'

    def get_queryset(self):
        """Get a list of scenarios for the current user."""
        user = self.request.user
        return Scenario.objects.filter(created_by=user)


class ScenarioCreate(LoginRequiredMixin, CreateView):
    """Scenario Create view."""

    form_class = ScenarioForm
    template_name = 'scenario/scenario_create.html'

    def get_success_url(self, *args, **kwargs):
        """
        On successful Scenario creation, automatically redirect users
        to the first page in the scenario wizard.
        """
        return reverse_lazy('conditions_create', args=(self.object.id,))


class ScenarioDetail(LoginRequiredMixin, DetailView):
    """Scenario Detail view."""

    model = Scenario
    template_name = 'scenario/scenario_detail.html'


class ConditionsCreate(LoginRequiredMixin, CreateView):
    """Scenario Conditions Create view."""

    form_class = ConditionForm
    template_name = 'scenario/conditions_create.html'

    def get_context_data(self, *args, **kwargs):
        """Override default context to return the proper scenario step."""
        ctx = super().get_context_data(*args, **kwargs)
        ctx['step_num'] = 0
        ctx['hide_first_half']
        ctx['hide_second_half']
        ctx = get_steps(ctx, ctx['step_num'])
        return ctx


class ConditionsDetail(LoginRequiredMixin, DetailView):
    """Scenario Conditions Detail view."""

    model = Condition
    template_name = 'scenario/conditions_detail.html'

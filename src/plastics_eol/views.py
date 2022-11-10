# views.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import ScenarioForm
from .models import Condition, ExportedPlastic, ImportedPlastic, \
    ReExportedPlastic, MSWComposition, MSWCompost, MSWIncineration, \
    MSWLandfill, MSWRecycling, PlasticIncineration, PlasticLandfill, \
    PlasticRecycling, PlasticReportedRecycled, Scenario


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
        if kwargs is not None:
            return reverse_lazy('detail', kwargs={'pk': kwargs['idnumber']})
        else:
            return reverse_lazy('detail', args=(self.object.id,))


class ScenarioDetail(LoginRequiredMixin, DetailView):
    """Scenario Detail view."""

    model = Scenario
    template_name = 'scenario/scenario_detail.html'

    def get_context_data(self, *args, **kwargs):
        GREEN = 'text-green'
        OKAY = 'check_circle'
        RED = 'text-red'
        BAD = 'cancel'

        ctx = super().get_context_data(*args, **kwargs)
        obj = self.object

        # # # Check each of the required inputs for a Scenario to be valid:
        # # ctx['conditions'] = Condition.objects.filter(scenario_id=pk).first()
        # ctx['condition_color'] = GREEN if obj.condition else RED
        # ctx['condition_icon'] = OKAY if obj.condition else BAD

        # # ctx['msw_composition'] = MSWComposition.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['msw_composition_color'] = GREEN if obj.MSWComposition else RED
        # ctx['msw_composition_icon'] = OKAY if obj.MSWComposition else BAD

        # # ctx['msw_recyc'] = MSWRecycling.objects.filter().first()
        # ctx['msw_recyc_color'] = GREEN if obj.MSWRecycling else RED
        # ctx['msw_recyc_icon'] = OKAY if obj.MSWRecycling else BAD

        # # ctx['msw_incin'] = MSWIncineration.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['msw_incin_color'] = GREEN if obj.MSWIncineration else RED
        # ctx['msw_incin_icon'] = OKAY if obj.MSWIncineration else BAD

        # # ctx['msw_landfill'] = MSWLandfill.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['msw_landfill_color'] = GREEN if obj.MSWLandfill else RED
        # ctx['msw_landfill_icon'] = OKAY if obj.MSWLandfill else BAD

        # # ctx['msw_compost'] = MSWCompost.objects.filter(scenario_id=pk).first()
        # ctx['msw_compost_color'] = GREEN if obj.MSWCompost else RED
        # ctx['msw_compost_icon'] = OKAY if obj.MSWCompost else BAD

        # # ctx['plastic_recyc'] = PlasticRecycling.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_recyc_color'] = GREEN if obj.PlasticRecycling else RED
        # ctx['plastic_recyc_icon'] = OKAY if obj.PlasticRecycling else BAD

        # # ctx['plastic_incin'] = PlasticIncineration.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_incin_color'] = GREEN if obj.PlasticIncineration else RED
        # ctx['plastic_incin_icon'] = OKAY if obj.PlasticIncineration else BAD

        # # ctx['plastic_landfill'] = PlasticLandfill.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_landfill_color'] = GREEN if obj.PlasticLandfill else RED
        # ctx['plastic_landfill_icon'] = OKAY if obj.PlasticLandfill else BAD

        # # ctx['plastic_reported_recycled'] = \
        # #     PlasticReportedRecycled.objects.filter(scenario_id=pk).first()
        # ctx['plastic_reported_recycled_color'] = GREEN if obj.PlasticReportedRecycled else RED
        # ctx['plastic_reported_recycled_icon'] = OKAY if obj.PlasticReportedRecycled else BAD

        # # ctx['plastic_import'] = ImportedPlastic.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_import_color'] = GREEN if obj.ImportedPlastic else RED
        # ctx['plastic_import_icon'] = OKAY if obj.ImportedPlastic else BAD

        # # ctx['plastic_export'] = ExportedPlastic.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_export_color'] = GREEN if obj.ExportedPlastic else RED
        # ctx['plastic_export_icon'] = OKAY if obj.ExportedPlastic else BAD

        # # ctx['plastic_re_export'] = ReExportedPlastic.objects.filter(
        # #     scenario_id=pk).first()
        # ctx['plastic_re_export_color'] = GREEN if obj.ReExportedPlastic else RED
        # ctx['plastic_re_export_icon'] = OKAY if obj.ReExportedPlastic else BAD

        return ctx


class ConditionsCreate(LoginRequiredMixin, CreateView):
    """Scenario Conditions Create view."""

    model = Condition


class ConditionsDetail(LoginRequiredMixin, DetailView):
    """Scenario Conditions Detail view."""

    model = Condition

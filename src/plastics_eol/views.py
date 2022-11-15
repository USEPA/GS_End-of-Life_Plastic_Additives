# views.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import ConditionForm, MSWCompositionForm, MSWCompostForm, \
    MSWIncinerationForm, MSWLandfillForm, MSWRecyclingForm, \
    ScenarioForm, PlasticRecyclingForm, PlasticIncinerationForm, \
    PlasticLandfillForm, PlasticReportedRecycledForm, \
    ImportedPlasticForm, ExportedPlasticForm, ReExportedPlasticForm

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


class WizardCreatePartial(LoginRequiredMixin, CreateView):
    """Custom partial class to contain constant pieces of other classes."""

    def get_context_data(self, *args, **kwargs):
        """Override default context to return the proper scenario step."""
        ctx = super().get_context_data(*args, **kwargs)
        ctx['page_title'] = self.page_title
        ctx['step_num'] = self.step_num
        ctx = get_steps(ctx, ctx['step_num'])
        return ctx

    def form_valid(self, form):
        """Override default form validator to add scenario_id"""
        obj = form.save(commit=False)
        obj.scenario_id = self.kwargs['pk']
        return super(WizardCreatePartial, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        """
        On successful Scenario creation, automatically redirect users
        to the next page in the scenario wizard.
        """
        return reverse_lazy(self.next_url, args=(self.object.scenario_id,))


class ConditionsCreate(WizardCreatePartial):
    """Scenario Conditions Create view."""

    form_class = ConditionForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Condition'
    step_num = 0
    next_url = 'msw_composition_create'


class ConditionsDetail(LoginRequiredMixin, DetailView):
    """Scenario Conditions Detail view."""

    model = Condition
    template_name = 'scenario/conditions_detail.html'


class MSWCompositionCreate(WizardCreatePartial):
    """Scenario MSWComposition Create view."""

    form_class = MSWCompositionForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'MSW Composition'
    step_num = 1
    next_url = 'msw_recycling_create'


class MSWRecyclingCreate(WizardCreatePartial):
    """Scenario MSW Recycling Create view."""

    form_class = MSWRecyclingForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'MSW Recycling'
    step_num = 2
    next_url = 'msw_incineration_create'


class MSWIncinerationCreate(WizardCreatePartial):
    """Scenario MSWIncineration Create view."""

    form_class = MSWIncinerationForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'MSW Incineration'
    step_num = 3
    next_url = 'msw_landfill_create'


class MSWLandfillCreate(WizardCreatePartial):
    """Scenario MSWLandfill Create view."""

    form_class = MSWLandfillForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'MSW Landfill'
    step_num = 4
    next_url = 'msw_compost_create'


class MSWCompostCreate(WizardCreatePartial):
    """Scenario MSWCompost Create view."""

    form_class = MSWCompostForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'MSW Compost'
    step_num = 5
    next_url = 'plastic_recycling_create'


class PlasticRecyclingCreate(WizardCreatePartial):
    """Scenario Plastic Recycling Create view."""

    form_class = PlasticRecyclingForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Recycling'
    step_num = 6
    next_url = 'plastic_incineration_create'


class PlasticIncinerationCreate(WizardCreatePartial):
    """Scenario Plastic Incineration Create view."""

    form_class = PlasticIncinerationForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Incineration'
    step_num = 7
    next_url = 'plastic_landfill_create'


class PlasticLandfillCreate(WizardCreatePartial):
    """Scenario Plastic Landfill Create view."""

    form_class = PlasticLandfillForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Landfill'
    step_num = 8
    next_url = 'plastic_reported_create'


class PlasticReportedCreate(WizardCreatePartial):
    """Scenario Plastic Reported Create view."""

    form_class = PlasticReportedRecycledForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Reported'
    step_num = 9
    next_url = 'plastic_imported_create'


class PlasticImportCreate(WizardCreatePartial):
    """Scenario Plastic Import Create view."""

    form_class = ImportedPlasticForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Import'
    step_num = 10
    next_url = 'plastic_exported_create'


class PlasticExportCreate(WizardCreatePartial):
    """Scenario Plastic Export Create view."""

    form_class = ExportedPlasticForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Export'
    step_num = 11
    next_url = 'plastic_reexported_create'


class PlasticReExportCreate(WizardCreatePartial):
    """Scenario Plastic ReExport Create view."""

    form_class = ReExportedPlasticForm
    template_name = 'scenario/_generic_inputs_create.html'
    page_title = 'Plastic Re-Export'
    step_num = 12
    next_url = 'RUN CALCULATIONS'

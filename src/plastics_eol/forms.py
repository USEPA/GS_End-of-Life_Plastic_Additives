# forms.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""
Forms related to Plastics EoL models.
"""

from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Condition, Scenario


USEPA_TEXT_ATTRS = {'class': 'usa-input mb-2'}


class ScenarioForm(forms.ModelForm):
    """Form for creating a Plastics EoL Scenario."""

    name = forms.CharField(widget=forms.TextInput(USEPA_TEXT_ATTRS),
                           label=_("Scenario Name:"), required=True)

    description = forms.CharField(widget=forms.TextInput(USEPA_TEXT_ATTRS),
                                  label=_("Scenario Description:"),
                                  required=False)

    class Meta:
        """Meta data for Scenario Form."""

        model = Scenario
        fields = ('name', 'description')

    def form_valid(self, form):
        """
        Custom form valid method to add created_by (requesting user)
        and date created (datetime.now).
        """
        form.instance.created_by = self.request.user
        form.instance.date = datetime.now()
        return super().form_valid(form)


class ConditionForm(forms.ModelForm):
    """Form representing a Scenario's Conditions inputs."""

    total_msw = forms.FloatField(
        label=_("Total MSW (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    total_waste = forms.FloatField(
        label=_("Total Plastic Waste (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    total_recyc = forms.FloatField(
        label=_("Total Plastic Recycled (Fraction, Domestic and Export):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    domestic_recyc = forms.FloatField(
        label=_("Plastic Recycled Domestically (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    export = forms.FloatField(
        label=_("Plastic Export Fraction (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    re_export = forms.FloatField(
        label=_("Plastic Re-Export (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    recyc_efficiency = forms.FloatField(
        label=_("Plastic Recycling Efficiency (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    incinerated = forms.FloatField(
        label=_("Plastic Incinerated (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    landfilled = forms.FloatField(
        label=_("Plastic Landfilled (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    waste_facility_emissions = forms.FloatField(
        label=_("Waste Facility Emissions (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    landfill_emissions = forms.FloatField(
        label=_("Emissions from Landfill (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    class Meta:
        """Meta data for Scenario Form."""

        model = Condition
        fields = (
            'total_msw', 'total_waste', 'total_recyc', 'domestic_recyc',
            'export', 're_export', 'recyc_efficiency', 'incinerated',
            'landfilled', 'waste_facility_emissions', 'landfill_emissions')

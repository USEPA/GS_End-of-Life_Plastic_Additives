# forms.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""
Forms related to Plastics EoL models.
"""

from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Condition, MSWComposition, MSWCompost, MSWIncineration, \
    MSWLandfill, MSWRecycling, Scenario, \
    PlasticRecycling, PlasticIncineration, PlasticLandfill, \
    PlasticReportedRecycled, ImportedPlastic, ExportedPlastic, \
    ReExportedPlastic


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
        """Meta data for Conditions inputs Form."""

        model = Condition
        fields = (
            'total_msw', 'total_waste', 'total_recyc', 'domestic_recyc',
            'export', 're_export', 'recyc_efficiency', 'incinerated',
            'landfilled', 'waste_facility_emissions', 'landfill_emissions')


class MSWCompositionForm(forms.ModelForm):
    """Form representing a Scenario's MSW Composition inputs."""

    inorganic = forms.FloatField(
        label=_("Misc. Inorganic Waste (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    other = forms.FloatField(
        label=_("Other (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    yard_trimmings = forms.FloatField(
        label=_("Yard Trimmings (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    food = forms.FloatField(
        label=_("Food (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    rubber_leather_textiles = forms.FloatField(
        label=_("Rubber, Leather, Textiles (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    wood = forms.FloatField(
        label=_("Wood (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    metals = forms.FloatField(
        label=_("Metals (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    glass = forms.FloatField(
        label=_("Glass (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    paper = forms.FloatField(
        label=_("Paper and Paperboard (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    plastics = forms.FloatField(
        label=_("Plastics (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    class Meta:
        """Meta data for Scenario MSW Composition inputs form."""
        model = MSWComposition
        fields = (
            'inorganic', 'other', 'yard_trimmings', 'food',
            'rubber_leather_textiles', 'wood', 'metals',
            'glass', 'paper', 'plastics'
        )


class MSWTotalsForm(MSWCompositionForm):
    """Form representing a Scenario's MSW Recycling inputs."""

    total_mass = forms.FloatField(
        label=_("Total Recycled Mass:"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    class Meta:
        fields = (
            'total_mass', 'inorganic', 'other', 'yard_trimmings', 'food',
            'rubber_leather_textiles', 'wood', 'metals',
            'glass', 'paper', 'plastics'
        )


class MSWRecyclingForm(MSWTotalsForm):
    """Form representing a Scenario's MSW Recycling inputs."""

    class Meta:
        """Meta data for Scenario MSW Composition inputs form."""
        model = MSWRecycling
        fields = MSWTotalsForm.Meta.fields


class MSWIncinerationForm(MSWTotalsForm):
    """Form representing a Scenario's MSW Incineration inputs."""

    class Meta:
        """Meta data for Scenario MSW Composition inputs form."""
        model = MSWIncineration
        fields = MSWTotalsForm.Meta.fields


class MSWLandfillForm(MSWTotalsForm):
    """Form representing a Scenario's MSW Landfill inputs."""

    class Meta:
        """Meta data for Scenario MSW Composition inputs form."""
        model = MSWLandfill
        fields = MSWTotalsForm.Meta.fields


class MSWCompostForm(MSWTotalsForm):
    """Form representing a Scenario's MSW Compost inputs."""

    class Meta:
        """Meta data for Scenario MSW Composition inputs form."""
        model = MSWCompost
        fields = MSWTotalsForm.Meta.fields


class PlasticsGenericForm(forms.ModelForm):
    """Class representing various plastic proportions in a scenario."""

    pet = forms.FloatField(
        label=_("PET Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    hdpe = forms.FloatField(
        label=_("HDPE Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    pvc = forms.FloatField(
        label=_("PVC Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    ldpe = forms.FloatField(
        label=_("LDPE Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    pla = forms.FloatField(
        label=_("PLA Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    pp = forms.FloatField(
        label=_("PP Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    ps = forms.FloatField(
        label=_("PS Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    other = forms.FloatField(
        label=_("Other Plastics Proportion (Fraction):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    class Meta:
        fields = ('pet', 'hdpe', 'pvc', 'ldpe', 'pal', 'pp', 'ps', 'other')


class PlasticRecyclingForm(PlasticsGenericForm):

    class Meta:
        model = PlasticRecycling
        fields = PlasticsGenericForm.Meta.fields


class PlasticIncinerationForm(PlasticsGenericForm):

    class Meta:
        model = PlasticIncineration
        fields = PlasticsGenericForm.Meta.fields


class PlasticLandfillForm(PlasticsGenericForm):

    class Meta:
        model = PlasticLandfill
        fields = PlasticsGenericForm.Meta.fields


class PlasticReportedRecycledForm(PlasticsGenericForm):

    class Meta:
        model = PlasticReportedRecycled
        fields = PlasticsGenericForm.Meta.fields


class ImportExportGenericForm(forms.ModelForm):
    """Generic form for import/export inputs."""

    ethylene = forms.FloatField(
        label=_("Ethylene (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    vinyl_chloride = forms.FloatField(
        label=_("Vinyl Chloride Mass (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    styrene = forms.FloatField(
        label=_("Styrene Mass (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))
    other = forms.FloatField(
        label=_("Other Plastics (Tons):"),
        widget=forms.NumberInput({'class': 'usa-input mb-2'}))

    class Meta:
        fields = ('ethylene', 'vinyl_chloride', 'styrene', 'other')


class ImportedPlasticForm(ImportExportGenericForm):

    class Meta:
        model = ImportedPlastic
        fields = ImportExportGenericForm.Meta.fields


class ExportedPlasticForm(ImportExportGenericForm):

    class Meta:
        model = ExportedPlastic
        fields = ImportExportGenericForm.Meta.fields


class ReExportedPlasticForm(ImportExportGenericForm):

    class Meta:
        model = ExportedPlastic
        fields = ImportExportGenericForm.Meta.fields

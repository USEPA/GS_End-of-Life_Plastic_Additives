# models.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of models."""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from .constants import *
from accounts.models import User


class Scenario(models.Model):
    """Class representing a calculator scenario."""

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(blank=False, null=False,
                                default=timezone.now)
    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('scenario_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Condition(models.Model):
    """User inputs for calculator Conditions (in fractions)."""
    scenario = models.OneToOneField(Scenario,
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    total_msw = models.FloatField(null=False, blank=False, default=0.0)
    total_waste = models.FloatField(null=False, blank=False, default=0.0)
    total_recyc = models.FloatField(null=False, blank=False, default=0.0)
    domestic_recyc = models.FloatField(null=False, blank=False, default=0.0)
    export = models.FloatField(null=False, blank=False, default=0.0)
    re_export = models.FloatField(null=False, blank=False, default=0.0)
    recyc_efficiency = models.FloatField(null=False, blank=False, default=0.0)
    incinerated = models.FloatField(null=False, blank=False, default=0.0)
    landfilled = models.FloatField(null=False, blank=False, default=0.0)
    waste_facility_emissions = models.FloatField(null=False,
                                                 blank=False,
                                                 default=0.0)
    landfill_emissions = models.FloatField(null=False,
                                           blank=False,
                                           default=0.0)


class MSWGeneric(models.Model):
    """Generic fields shared with most MSW User Specification classes."""
    scenario = models.OneToOneField(Scenario,
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    inorganic = models.FloatField(null=False, blank=False, default=0.0)
    other = models.FloatField(null=False, blank=False, default=0.0)
    yard_trimmings = models.FloatField(null=False, blank=False, default=0.0)
    food = models.FloatField(null=False, blank=False, default=0.0)
    rubber_leather_textiles = models.FloatField(null=False,
                                                blank=False,
                                                default=0.0)
    wood = models.FloatField(null=False, blank=False, default=0.0)
    metals = models.FloatField(null=False, blank=False, default=0.0)
    glass = models.FloatField(null=False, blank=False, default=0.0)
    paper = models.FloatField(null=False, blank=False, default=0.0)
    plastics = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        abstract = True


class MSWComposition(MSWGeneric):
    """User specifications for Municipal Solid Waste Composition."""


class MSWRecycling(MSWGeneric):
    """User Specifications for Recycling Data."""
    total_mass = models.FloatField(null=False, blank=False, default=0.0)


class MSWIncineration(MSWGeneric):
    """User Specifications for Incineration Data."""
    total_mass = models.FloatField(null=False, blank=False, default=0.0)


class MSWLandfill(MSWGeneric):
    """User Specifications for Landfill Data."""
    total_mass = models.FloatField(null=False, blank=False, default=0.0)


class MSWCompost(MSWGeneric):
    """User Specifications for Compost Data."""
    total_mass = models.FloatField(null=False, blank=False, default=0.0)


class PlasticGeneric(models.Model):
    """Generic fields shared with most Plastic User Specification classes."""
    scenario = models.OneToOneField(Scenario,
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    pet = models.FloatField(null=False, blank=False, default=0.0)
    hdpe = models.FloatField(null=False, blank=False, default=0.0)
    pvc = models.FloatField(null=False, blank=False, default=0.0)
    ldpe = models.FloatField(null=False, blank=False, default=0.0)
    pal = models.FloatField(null=False, blank=False, default=0.0)
    pp = models.FloatField(null=False, blank=False, default=0.0)
    ps = models.FloatField(null=False, blank=False, default=0.0)
    other = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        abstract = True


class PlasticRecycling(PlasticGeneric):
    """User Specifications for Plastic Recycled Proportions (fractions)"""


class PlasticIncineration(PlasticGeneric):
    """User Specifications for Plastic Incinerated Proportions (fractions)"""


class PlasticLandfill(PlasticGeneric):
    """User Specifications for Plastic Landfilled Proportions (fractions)"""


class PlasticReportedRecycled(PlasticGeneric):
    """User Specifications for Plastic Reported Recycled Masses (tons)"""


class ImportExportGeneric(models.Model):
    """
    Generic fields shared with most
    Plastic Import/Export User Specification classes.
    """
    scenario = models.OneToOneField(Scenario,
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    ethylene = models.FloatField(null=False, blank=False, default=0.0)
    vinyl_chloride = models.FloatField(null=False, blank=False, default=0.0)
    styrene = models.FloatField(null=False, blank=False, default=0.0)
    other = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        abstract = True


class ImportedPlastic(ImportExportGeneric):
    """User Specifications for Plastic Imported Masses."""


class ExportedPlastic(ImportExportGeneric):
    """User Specifications for Plastic Exported Masses."""


class ReExportedPlastic(ImportExportGeneric):
    """User Specifications for Plastic Re-Exported Masses."""

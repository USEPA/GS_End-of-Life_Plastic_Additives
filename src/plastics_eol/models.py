# models.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of models."""

from django.db import models
from .constants import *


class GenericValue(models.Model):
    """Class representing a generic value of Year, Name, and Value."""
    year = models.IntegerField(null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        abstract = True


class ConditionValue(GenericValue):
    """
    Class containing DEFAULT Conditions Values for a given year.
    Represented by fields B2-B10 in the US 2018 Facts tab.
    """


class AssumedValue(GenericValue):
    """
    Class containing DEFAULT Assumed Values for a given year.
    Represented by fields B12-B18 in the US 2018 Facts tab.
    """


class MSWGenerated(GenericValue):
    """
    Class containing DEFAULT MSW Generated values for a given year.
    Represented by fields B20-B30 in the US 2018 Facts tab.
    """


class MSWRecycled(GenericValue):
    """
    Class containing DEFAULT MSW Recycled values for a given year.
    Represented by fields B32-B42 in the US 2018 Facts tab.
    """


class MSWIncinerated(GenericValue):
    """
    Class containing DEFAULT MSW Incinerated values for a given year.
    Represented by fields B44-B54 in the US 2018 Facts tab.
    """


class MSWLandfilled(GenericValue):
    """
    Class containing DEFAULT MSW Landfilled values for a given year.
    Represented by fields B56-B66 in the US 2018 Facts tab.
    """


class MSWComposted(GenericValue):
    """
    Class containing DEFAULT MSW Composted values for a given year.
    Represented by fields B68-B78 in the US 2018 Facts tab.
    """


class AshGenerated(GenericValue):
    """
    Class containing DEFAULT Ash content generated from plastic incineration.
    Represented by fields B95-B101 in the US 2018 Facts tab.
    """


class Emission(GenericValue):
    """
    Class representing an emission value. In addition to the Generic Value
    being inherited, this class also contains a subheading. The subheading can
    be compared to the name of each other class inheriting from Generic Value.
    For example, the subheading might be "Collection Emissions",
    "Emissions from Manufacture", etc.
    Represented by fields B80-B93 and B103-B108.
    """
    subheading = models.TextField(null=False, blank=False)

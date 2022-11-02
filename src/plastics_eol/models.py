# models.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of models."""

from django.db import models
from .constants import *




# class AssumedValue(models.Model):
#   """
#   Class containing a constant value from assumptions to be used in calculations.
#   """
#   name = models.TextField(null=False, blank=False)
#   value = models.FloatField(null=False, blank=False, default=0.0)

# class LowAdditiveFractions(models.Model):
#   """
#   Class containing low additive Fractions.
#   The name represents a type of additive and value is the bulk mass proportion.
#   """

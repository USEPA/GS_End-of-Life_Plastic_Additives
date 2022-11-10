# admin.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""
Define classes used to generate Django Admin portion of the website.
"""

from django.contrib import admin
from .models import Condition, ExportedPlastic, ImportedPlastic, \
    ReExportedPlastic, MSWComposition, MSWCompost, MSWIncineration, \
    MSWLandfill, MSWRecycling, PlasticIncineration, PlasticLandfill, \
    PlasticRecycling, PlasticReportedRecycled, Scenario

admin.site.register(Condition)

admin.site.register(ExportedPlastic)

admin.site.register(ImportedPlastic)

admin.site.register(ReExportedPlastic)

admin.site.register(MSWComposition)

admin.site.register(MSWCompost)

admin.site.register(MSWIncineration)

admin.site.register(MSWLandfill)

admin.site.register(MSWRecycling)

admin.site.register(PlasticIncineration)

admin.site.register(PlasticLandfill)

admin.site.register(PlasticRecycling)

admin.site.register(PlasticReportedRecycled)

admin.site.register(Scenario)

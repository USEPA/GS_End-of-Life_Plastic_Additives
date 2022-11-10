# forms.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""
Forms related to Plastics EoL models.
"""

from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Scenario


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

# views.py (disclaimers)
# !/usr/bin/env python3
# coding=utf-8

"""
Views for managing EPA disclaimers.

Available functions:
"""

from datetime import datetime
from django.http import HttpRequest
from django.shortcuts import render


def home(request):
    """Home page for the Disclaimers module."""
    assert isinstance(request, HttpRequest)
    ctx = {'title': 'Disclaimer', 'year': datetime.now().year}
    return render(request, 'disclaimers.html', ctx)

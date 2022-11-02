# urls.py (disclaimers)
# !/usr/bin/env python3
# coding=utf-8
# py-lint: disable=invalid-name
# We disable the invalid name because urlpatterns is the Django default.
# py-lint: disable=C0301

"""
Module related to urls for EPA disclaimers.

Available functions:
"""

from django.urls import re_path
from disclaimers.views import home

app_name = 'disclaimers'

urlpatterns = [
    re_path(r'^$', home, name='disclaimers'),
]

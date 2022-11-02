# context_processors.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of context processors for plastics_eol."""

from datetime import datetime
from plastics_eol.settings import APP_NAME, APP_NAME_SHORT, APP_VERSION


def selected_settings(request):
    """Return the version value as a dictionary."""
    # you can add other values here as well
    return {'year': datetime.now().year, 'APP_VERSION': APP_VERSION,
            'APP_NAME': APP_NAME, 'APP_NAME_SHORT': APP_NAME_SHORT}

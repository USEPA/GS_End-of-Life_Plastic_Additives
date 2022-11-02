# views.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Definition of views."""
from django.http import HttpRequest
from django.shortcuts import render


def home(request):
    """Render the home page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'index.html', {
        'title': 'Home Page',
    })


def contact(request):
    """Render the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 'main/contact.html', {
            'title': 'Contact',
            'message': 'Your contact page.',
        })


def about(request):
    """Render the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 'main/about.html', {
            'title': 'About',
            'message': 'Your application description page.',
        })

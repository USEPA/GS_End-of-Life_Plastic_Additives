# urls.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

from django.contrib import admin
from django.urls import path, include
from .views import home, contact, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('disclaimers/', include('disclaimers.urls', namespace='disclaimers')),
    path('support/', include('support.urls', namespace='support')),
    path('teams/', include('teams.urls', namespace='teams')),

    path('', home, name='home'),
    path('dashboard/', home, name='dashboard'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]

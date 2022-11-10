# urls.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

from django.contrib import admin
from django.urls import path, include
from .views import home, contact, about, ConditionsCreate, ConditionsDetail, \
    ScenarioCreate, ScenarioDetail, ScenarioList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('disclaimers/', include('disclaimers.urls', namespace='disclaimers')),
    path('support/', include('support.urls', namespace='support')),
    path('teams/', include('teams.urls', namespace='teams')),

    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),

    path('scenario/', ScenarioList.as_view(), name='scenario'),
    path('scenario/create/', ScenarioCreate.as_view(), name='scenario_create'),
    path('scenario/<int:pk>/',
         ScenarioDetail.as_view(),
         name='scenario_detail'),

    path('scenario/<int:pk>/conditions/',
         ConditionsDetail.as_view(),
         name='conditions_detail'),
    path('scenario/<int:pk>/conditions/create',
         ConditionsCreate.as_view(),
         name='conditions_create'),
]

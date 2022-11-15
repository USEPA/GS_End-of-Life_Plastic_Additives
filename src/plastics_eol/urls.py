# urls.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

from django.contrib import admin
from django.urls import path, include
from .views import home, contact, about, ConditionsCreate, ConditionsDetail, \
    MSWCompositionCreate, ScenarioCreate, ScenarioDetail, ScenarioList

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

    # path('scenario/<int:pk>/msw_composition/',
    #    MSWCompositionDetail.as_view(),
    #    name='msw_composition_detail'),
    path('scenario/<int:pk>/msw_composition/create',
         MSWCompositionCreate.as_view(),
         name='msw_composition_create'),

    # path('scenario/<int:pk>/msw_recycling/',
    #      MSWRecyclingDetail.as_view(),
    #      name='msw_recycling_detail'),
    # path('scenario/<int:pk>/msw_recycling/create',
    #      MSWRecyclingCreate.as_view(),
    #      name='msw_recycling_create'),

    # path('scenario/<int:pk>/msw_incineration/',
    #      MSWIncinerationDetail.as_view(),
    #      name='msw_incineration_detail'),
    # path('scenario/<int:pk>/msw_incineration/create',
    #      MSWIncinerationCreate.as_view(),
    #      name='msw_incineration_create'),

    # path('scenario/<int:pk>/msw_landfill/',
    #      MSWLandfillDetail.as_view(),
    #      name='msw_landfill_detail'),
    # path('scenario/<int:pk>/msw_landfill/create',
    #      MSWLandfillCreate.as_view(),
    #      name='msw_landfill_create'),

    # path('scenario/<int:pk>/msw_compost/',
    #      MSWCompostDetail.as_view(),
    #      name='msw_compost_detail'),
    # path('scenario/<int:pk>/msw_compost/create',
    #      MSWCompostCreate.as_view(),
    #      name='msw_compost_create'),

    # ################################################################

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),

    # path('scenario/<int:pk>/conditions/',
    #      ConditionsDetail.as_view(),
    #      name='conditions_detail'),
    # path('scenario/<int:pk>/conditions/create',
    #      ConditionsCreate.as_view(),
    #      name='conditions_create'),
]

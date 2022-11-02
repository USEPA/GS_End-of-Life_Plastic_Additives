# tests.py (disclaimers)
# !/usr/bin/env python3
# coding=utf-8
# pylint: skip-file
# We skip this file because it wasn't written by/for EPA.
# py-lint: disable=C0301

"""Module related to tests for EPA disclaimers."""

from accounts.models import User
from django.test import Client, TestCase


class TestViews(TestCase):
    """Tests for the application views."""

    def setUp(self):
        """Test client user with generic password not on server."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_index_pass(self):
        """Test the index page can be accessed via HTTP GET."""
        response = self.client.get('/disclaimers/')
        self.assertContains(response, 'EPA Disclaimers', 3, 200)
        self.assertContains(response,
                            'Software Copyright Notices And Disclaimers', 1,
                            200)

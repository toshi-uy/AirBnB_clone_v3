#!/usr/bin/python3
"""client setup"""
import pytest
from api.v1.views import app_views
from api.v1 import app

@pytest.fixture
def client():
    """Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

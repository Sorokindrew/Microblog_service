import pytest
from src.app import application


@pytest.fixture
def app_():
    return application


@pytest.fixture
def client(app_):
    client_instance = app_.test_client()
    client_instance.environ_base['HTTP_API_KEY'] = 'test'
    return client_instance

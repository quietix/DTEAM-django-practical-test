from django.http import HttpResponse
import pytest
from rest_framework.test import APIClient
from audit.models import RequestLog


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_request_log_middleware(client: APIClient):
    response: HttpResponse = client.get("/")
    assert response.status_code == 200
    assert RequestLog.objects.count() == 1

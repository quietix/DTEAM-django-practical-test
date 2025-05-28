import pytest

from django.urls import reverse
from django.test.client import Client

from rest_framework.test import APIClient
from rest_framework.response import Response

from main.models import CV


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def dummy_cvs() -> list[CV]:
    return CV.objects.bulk_create(
        [
            CV(
                firstname="John",
                lastname="Doe",
                skills="Python, Django",
                projects="Project 1",
                bio="Test bio",
                contacts="test@example.com",
            ),
            CV(
                firstname="Alice",
                lastname="Smith",
                skills="JavaScript, React",
                projects="Project 2",
                bio="Another bio",
                contacts="alice@example.com",
            ),
        ]
    )


@pytest.fixture
def dummy_cv() -> CV:
    return CV.objects.create(
        firstname="John",
        lastname="Doe",
        skills="Python, Django",
        projects="Project 1",
        bio="Test bio",
        contacts="test@example.com",
    )


@pytest.mark.django_db
class TestCVListView:
    def test_list_view_loads_successfully(self, client: Client):
        response = client.get(reverse("main:cv-list"))
        assert response.status_code == 200
        assert "main/cv_list.html" in [t.name for t in response.templates]

    def test_list_contains_cvs(self, client: Client, dummy_cvs: list[CV]):
        response = client.get(reverse("main:cv-list"))
        assert "cvs" in response.context
        assert len(response.context["cvs"]) == 2


@pytest.mark.django_db
class TestCVDetailView:
    def test_detail_view_loads_successfully(self, client: Client, dummy_cv: CV):
        response = client.get(reverse("main:cv-detail", kwargs={"pk": dummy_cv.pk}))
        assert response.status_code == 200
        assert "main/cv_detail.html" in [t.name for t in response.templates]

    def test_detail_view_returns_404_for_invalid_cv(self, client: Client):
        response = client.get(reverse("main:cv-detail", kwargs={"pk": 1}))
        assert response.status_code == 404

    def test_detail_context_data(self, client: Client, dummy_cv: CV):
        response = client.get(reverse("main:cv-detail", kwargs={"pk": dummy_cv.pk}))
        cv = response.context.get("cv")
        assert cv is not None
        assert cv.pk == dummy_cv.pk


@pytest.mark.django_db
class TestCVViewSet:
    @pytest.fixture
    def create_data(self) -> dict:
        return {
            "firstname": "John",
            "lastname": "Doe",
            "skills": "Python, Django",
            "projects": "Project 1",
            "bio": "Test bio",
            "contacts": "test@example.com",
        }

    @pytest.fixture
    def update_data(self) -> dict:
        return {
            "firstname": "John",
            "lastname": "Doe",
            "skills": "Python, Django",
            "projects": "Project 1",
            "bio": "Test bio",
            "contacts": "test@example.com",
        }

    def test_viewset_list_view(self, api_client: APIClient, dummy_cvs: list[CV]):
        response: Response = api_client.get(reverse("main:cv-api-list"))
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["id"] == dummy_cvs[0].pk
        assert data[1]["id"] == dummy_cvs[1].pk

    def test_viewset_detail_view(self, api_client: APIClient, dummy_cv: CV):
        response: Response = api_client.get(reverse("main:cv-api-detail", kwargs={"pk": dummy_cv.pk}))
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == dummy_cv.pk
        assert data["firstname"] == dummy_cv.firstname
        assert data["lastname"] == dummy_cv.lastname

    def test_viewset_create_view(self, api_client: APIClient, create_data: dict):
        response: Response = api_client.post(reverse("main:cv-api-list"), data=create_data)
        data = response.json()
        assert response.status_code == 201
        assert data["id"] is not None
        assert data["firstname"] == create_data["firstname"]
        assert data["lastname"] == create_data["lastname"]
        assert data["skills"] == create_data["skills"]
        assert data["projects"] == create_data["projects"]
        assert data["bio"] == create_data["bio"]
        assert data["contacts"] == create_data["contacts"]

    def test_viewset_update_view(self, api_client: APIClient, dummy_cv: CV, update_data: dict):
        response: Response = api_client.put(
            reverse("main:cv-api-detail", kwargs={"pk": dummy_cv.pk}), data=update_data
        )
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == dummy_cv.pk
        assert data["firstname"] == update_data["firstname"]
        assert data["lastname"] == update_data["lastname"]
        assert data["skills"] == update_data["skills"]
        assert data["projects"] == update_data["projects"]

    def test_viewset_partial_update_view(
        self, api_client: APIClient, dummy_cv: CV, update_data: dict
    ):
        partial_update_data = {
            "firstname": "Partial Update Name",
        }
        response: Response = api_client.patch(
            reverse("main:cv-api-detail", kwargs={"pk": dummy_cv.pk}),
            data=partial_update_data,
        )
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == dummy_cv.pk
        assert data["firstname"] == partial_update_data["firstname"]
        assert data["lastname"] == dummy_cv.lastname
        assert data["skills"] == dummy_cv.skills
        assert data["projects"] == dummy_cv.projects
        assert data["bio"] == dummy_cv.bio
        assert data["contacts"] == dummy_cv.contacts

    def test_viewset_delete_view(self, api_client: APIClient, dummy_cv: CV):
        response: Response = api_client.delete(
            reverse("main:cv-api-detail", kwargs={"pk": dummy_cv.pk})
        )
        assert response.status_code == 204
        assert not CV.objects.filter(pk=dummy_cv.pk).exists()

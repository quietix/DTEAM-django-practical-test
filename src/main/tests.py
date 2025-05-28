import pytest
from django.urls import reverse
from django.test.client import Client
from main.models import CV


@pytest.fixture
def client() -> Client:
    return Client()


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

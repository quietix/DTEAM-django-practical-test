from django.urls import path
from main.views import CVListView, CVDetailView, cv_to_pdf


app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv-list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv-detail"),
    path("cv/download/<int:id>/", cv_to_pdf, name="cv-download"),
]

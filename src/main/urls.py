from django.urls import path
from main.views import (
    CVListView,
    CVDetailView,
    cv_to_pdf,
    CVViewSet,
    SettingsView,
    send_cv_email,
    translate_cv_view,
)
from rest_framework.routers import SimpleRouter


app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv-list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv-detail"),
    path("cv/download/<int:id>/", cv_to_pdf, name="cv-download"),
    path("cv/email/<int:id>/", send_cv_email, name="send-cv-email"),
    path("cv/translate/<int:id>/", translate_cv_view, name="translate-cv"),
    path("settings/", SettingsView.as_view(), name="settings"),
]

router = SimpleRouter()
router.register("api/cv", CVViewSet, basename="cv-api")
urlpatterns += router.urls

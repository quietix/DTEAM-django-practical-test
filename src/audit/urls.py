from django.urls import path
from audit.views import LogsListView

app_name = "audit"

urlpatterns = [
    path("logs/", LogsListView.as_view(), name="logs-list"),
]

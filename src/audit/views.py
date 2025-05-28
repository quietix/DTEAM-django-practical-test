from django.views.generic import ListView
from audit.models import RequestLog


class LogsListView(ListView):
    model = RequestLog
    template_name = "audit/logs_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        return RequestLog.objects.all()[:10]

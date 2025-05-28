from audit.models import RequestLog
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            with transaction.atomic():
                RequestLog.objects.create(
                    http_method=request.method,
                    path=request.path,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    user=request.user if request.user.is_authenticated else None,
                    query_string=request.META.get("QUERY_STRING"),
                )
        except Exception as e:
            logger.error(f"Failed to log request: {str(e)}")
            
        response = self.get_response(request)
        return response

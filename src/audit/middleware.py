from audit.models import RequestLog
import logging
from django.db import DatabaseError, IntegrityError
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            RequestLog.objects.create(
                http_method=request.method,
                path=request.path,
                ip_address=request.META.get("REMOTE_ADDR"),
                user=request.user if request.user.is_authenticated else None,
                query_string=request.META.get("QUERY_STRING"),
            )
        except ValidationError as e:
            logger.error(f"Validation error while logging request: {str(e)}")
        except IntegrityError as e:
            logger.error(f"Database integrity error while logging request: {str(e)}")
        except DatabaseError as e:
            logger.error(f"Database error while logging request: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while logging request: {str(e)}")

        response = self.get_response(request)
        return response

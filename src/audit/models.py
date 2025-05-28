from django.db import models
from django.contrib.auth.models import User


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    http_method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query_string = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.path}"

    class Meta:
        ordering = ['-timestamp']

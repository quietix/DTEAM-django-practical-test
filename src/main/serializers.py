from rest_framework import serializers

from main.models import CV


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = [
            "id",
            "firstname",
            "lastname",
            "skills",
            "projects",
            "bio",
            "contacts",
        ]
        read_only_fields = ["id"]

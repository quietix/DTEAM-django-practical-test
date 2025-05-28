from rest_framework import serializers

from main.models import CV


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = "__all__"
        read_only_fields = ["id"]

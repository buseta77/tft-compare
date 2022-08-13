from rest_framework import serializers
from backend.models import UsersCompared


class UsersComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersCompared
        fields = ['username1', 'username2', 'server', 'compared_at']


class ComparedDataSerializer(serializers.Serializer):
    avg1 = serializers.FloatField()
    avg2 = serializers.FloatField()
    created = serializers.DateTimeField()

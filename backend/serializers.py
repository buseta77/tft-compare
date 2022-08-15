from rest_framework import serializers
from backend.models import UsersCompared


class UsersComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersCompared
        fields = ['username1', 'username2', 'server', 'compared_at']

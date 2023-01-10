from rest_framework import serializers
from backend.models import UsersCompared, MatchInfo


class UsersComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersCompared
        fields = ['id', 'username1', 'username2', 'server', 'compared_at']


class MatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchInfo
        fields = ['match_id', 'server', 'match_data', 'created_at']

from rest_framework import serializers
from backend.models import UsersCompared


class UsersComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersCompared
        fields = ['username1', 'username2', 'server', 'compared_at']


class ComparedDataSerializer(serializers.Serializer):
    user1_avg = serializers.FloatField()
    user2_avg = serializers.FloatField()
    user1_first = serializers.IntegerField()
    user2_first = serializers.IntegerField()
    user1_top4 = serializers.IntegerField()
    user2_top4 = serializers.IntegerField()
    user1_eight = serializers.IntegerField()
    user2_eight = serializers.IntegerField()
    user1_tier = serializers.CharField()
    user2_tier = serializers.CharField()
    user1_points = serializers.IntegerField()
    user2_points = serializers.IntegerField()
    user1_total_wins = serializers.IntegerField()
    user2_total_wins = serializers.IntegerField()
    user1_total_losses = serializers.IntegerField()
    user2_total_losses = serializers.IntegerField()
    played_together = serializers.IntegerField()
    created = serializers.DateTimeField()

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class UsersCompared(models.Model):
    username1 = models.CharField(max_length=100, blank=False)
    username2 = models.CharField(max_length=100, blank=False)
    server = models.CharField(max_length=50, blank=False)
    compared_at = models.DateTimeField(auto_now_add=True)


class MatchInfo(models.Model):
    match_id = models.CharField(max_length=100, blank=False)
    server = models.CharField(max_length=50, blank=False)
    match_data = models.CharField(max_length=999999, blank=False)
    created_at = models.DateTimeField()

    @staticmethod
    def game_exists(game, server):
        try:
            match = MatchInfo.objects.get(match_id=game, server=server)
            data = getattr(match, "match_data")
            return data
        except ObjectDoesNotExist:
            return None

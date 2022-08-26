import json

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


class StaticInfo(models.Model):
    data = models.CharField(max_length=999999)
    info = models.CharField(max_length=50)

    @staticmethod
    def get_champ_name(champion_id):
        raw_data = StaticInfo.objects.get(info='set7-champions')
        data = getattr(raw_data, "data")
        data_json = json.loads(data)
        for item in data_json:
            if item['championId'] == champion_id:
                return item['name']
        return None

    @staticmethod
    def get_item_name(item_id):
        raw_data = StaticInfo.objects.get(info='set7-items')
        data = getattr(raw_data, "data")
        data_json = json.loads(data)
        for item in data_json:
            if item['id'] == item_id:
                return item['name']
        return None

    @staticmethod
    def get_trait_name(trait_id):
        raw_data = StaticInfo.objects.get(info='set7-traits')
        data = getattr(raw_data, "data")
        data_json = json.loads(data)
        for item in data_json:
            if item['key'] == trait_id:
                return item['name']
        return None

import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from riotwatcher import TftWatcher
from backend.serializers import UsersComparedSerializer, ComparedDataSerializer
from backend.models import UsersCompared
from requests.exceptions import HTTPError
from statistics import mean
from datetime import datetime


def convert_server(server_abbreviation):
    if server_abbreviation in ['euw1', 'eun1', 'ru']:
        return 'europe'
    elif server_abbreviation in ['br1', 'la1', 'la2', 'na1']:
        return 'americas'
    elif server_abbreviation in ['jp1', 'kr', 'tr1']:
        return 'asia'
    elif server_abbreviation in ['oc1']:
        return 'sea'
    else:
        return None


class ComparedData:
    def __init__(self, user1_avg, user2_avg, user1_first, user2_first, user1_top4, user2_top4, user1_eight,
                 user2_eight, user1_tier, user2_tier, user1_points, user2_points, user1_total_wins, user2_total_wins,
                 user1_total_losses, user2_total_losses):
        self.user1_avg = user1_avg
        self.user2_avg = user2_avg
        self.user1_first = user1_first
        self.user2_first = user2_first
        self.user1_top4 = user1_top4
        self.user2_top4 = user2_top4
        self.user1_eight = user1_eight
        self.user2_eight = user2_eight
        self.user1_tier = user1_tier
        self.user2_tier = user2_tier
        self.user1_points = user1_points
        self.user2_points = user2_points
        self.user1_total_wins = user1_total_wins
        self.user2_total_wins = user2_total_wins
        self.user1_total_losses = user1_total_losses
        self.user2_total_losses = user2_total_losses
        self.created = datetime.now()


# Create your views here
class GamesTogether(APIView):
    def get(self, request):
        data = UsersCompared.objects.all()
        serializer = UsersComparedSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        users_data = request.data
        watcher = TftWatcher(os.environ.get("RIOT_KEY"))

        try:
            user1 = watcher.summoner.by_name(users_data['server'], users_data['username1'])
            user2 = watcher.summoner.by_name(users_data['server'], users_data['username2'])
        except HTTPError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        match_list_user1 = watcher.match.by_puuid(convert_server(users_data['server']), user1['puuid'], count=200)
        match_list_user2 = watcher.match.by_puuid(convert_server(users_data['server']), user2['puuid'], count=200)
        common_match_list = list(set(match_list_user1).intersection(match_list_user2))
        user1_placements, user2_placements, matches = [], [], []
        user1_first, user1_top4, user1_eight, user2_first, user2_top4, user2_eight = 0, 0, 0, 0, 0, 0

        for elt in common_match_list:
            match = watcher.match.by_id(convert_server(users_data['server']), elt)
            matches.append(match)
            for participant in match['info']['participants']:
                if participant['puuid'] == user1['puuid']:
                    user1_placements.append(participant['placement'])
                    if participant['placement'] == 1:
                        user1_first += 1
                    if participant['placement'] < 5:
                        user1_top4 += 1
                    if participant['placement'] == 8:
                        user1_eight += 1
                if participant['puuid'] == user2['puuid']:
                    user2_placements.append(participant['placement'])
                    if participant['placement'] == 1:
                        user2_first += 1
                    if participant['placement'] < 5:
                        user2_top4 += 1
                    if participant['placement'] == 8:
                        user2_eight += 1

        user1_avg = mean(user1_placements)
        user2_avg = mean(user2_placements)

        user1_info = watcher.league.by_summoner(users_data['server'], user1['id'])
        user2_info = watcher.league.by_summoner(users_data['server'], user2['id'])

        user1_tier = user1_info['tier']
        user2_tier = user2_info['tier']
        user1_points = user1_info['leaguePoints']
        user2_points = user2_info['leaguePoints']
        user1_total_wins = user1_info['wins']
        user2_total_wins = user2_info['wins']
        user1_total_losses = user1_info['losses']
        user2_total_losses = user2_info['losses']

        response_data = ComparedData(user1_avg=user1_avg,
                                     user2_avg=user2_avg,
                                     user1_first=user1_first,
                                     user2_first=user2_first,
                                     user1_top4=user1_top4,
                                     user2_top4=user2_top4,
                                     user1_eight=user1_eight,
                                     user2_eight=user2_eight,
                                     user1_tier=user1_tier,
                                     user2_tier=user2_tier,
                                     user1_points=user1_points,
                                     user2_points=user2_points,
                                     user1_total_wins=user1_total_wins,
                                     user2_total_wins=user2_total_wins,
                                     user1_total_losses=user1_total_losses,
                                     user2_total_losses=user2_total_losses)
        response_serialized = ComparedDataSerializer(response_data)

        serializer = UsersComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_serialized.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

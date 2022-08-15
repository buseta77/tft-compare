import os
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework import status
from riotwatcher import TftWatcher
from backend.serializers import UsersComparedSerializer
from backend.models import UsersCompared
from requests.exceptions import HTTPError
from statistics import mean
from datetime import datetime
from django.shortcuts import render


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


# Create your views here
class Home(View):
    def get(self, request):
        return render(request, 'home.html')


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
        if not common_match_list:
            return Response({})
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
        played_together = len(common_match_list)

        try:
            user1_tier = str(user1_info[0]['tier'])
            user2_tier = str(user2_info[0]['tier'])
            user1_points = int(user1_info[0]['leaguePoints'])
            user2_points = int(user2_info[0]['leaguePoints'])
            user1_total_wins = int(user1_info[0]['wins'])
            user2_total_wins = int(user2_info[0]['wins'])
            user1_total_losses = int(user1_info[0]['losses'])
            user2_total_losses = int(user2_info[0]['losses'])
        except IndexError:
            user1_tier = None
            user2_tier = None
            user1_points = None
            user2_points = None
            user1_total_wins = None
            user2_total_wins = None
            user1_total_losses = None
            user2_total_losses = None
        except ValueError:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        response_data = {'user1': {
                                'avg': user1_avg,
                                'first': user1_first,
                                'top4': user1_top4,
                                'eight': user1_eight,
                                'league': user1_tier,
                                'points': user1_points,
                                'total_wins': user1_total_wins,
                                'total_losses': user1_total_losses,
                                'pp': f'https://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/{user1["profileIconId"]}.png',
                                'level': user1['summonerLevel']},
                         'user2': {
                                'avg': user2_avg,
                                'first': user2_first,
                                'top4': user2_top4,
                                'eight': user2_eight,
                                'league': user2_tier,
                                'points': user2_points,
                                'total_wins': user2_total_wins,
                                'total_losses': user2_total_losses,
                                'pp': f'https://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/{user2["profileIconId"]}.png',
                                'level': user2['summonerLevel']},
                         'played_together': played_together,
                         'created': datetime.now()}
        serializer = UsersComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

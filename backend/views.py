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
import configparser


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
    def __init__(self, avg1, avg2):
        self.avg1 = avg1
        self.avg2 = avg2
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
        user1_placements, user2_placements, matches = [], [], []

        #for i in range(len(match_list_user1)):
        for i in range(40):
            match = watcher.match.by_id(convert_server(users_data['server']), match_list_user1[i])
            participants = match['metadata']['participants']
            for player in participants:
                if player == user2['puuid']:
                    matches.append(match)
                    for participant in match['info']['participants']:
                        if participant['puuid'] == user1['puuid']:
                            user1_placements.append(participant['placement'])
                        if participant['puuid'] == user2['puuid']:
                            user2_placements.append(participant['placement'])
        #for i in range(len(match_list_user2)):
        for i in range(40):
            match = watcher.match.by_id(convert_server(users_data['server']), match_list_user2[i])
            participants = match['metadata']['participants']
            for player in participants:
                if player == user1['puuid']:
                    if match not in matches:
                        matches.append(match)
                        for participant in match['info']['participants']:
                            if participant['puuid'] == user1['puuid']:
                                user1_placements.append(participant['placement'])
                            if participant['puuid'] == user2['puuid']:
                                user2_placements.append(participant['placement'])

        user1_avg = mean(user1_placements)
        user2_avg = mean(user2_placements)

        response_data = ComparedData(avg1=user1_avg, avg2=user2_avg)
        response_serialized = ComparedDataSerializer(response_data)

        serializer = UsersComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_serialized.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

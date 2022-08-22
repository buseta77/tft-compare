import json
import os
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework import status
from riotwatcher import TftWatcher
from backend.serializers import UsersComparedSerializer, MatchInfoSerializer
from backend.models import UsersCompared, MatchInfo
from requests.exceptions import HTTPError
from statistics import mean
from django.shortcuts import render
from datetime import datetime


def convert_server(server_abbreviation):
    if server_abbreviation in ['euw1', 'eun1', 'ru', 'tr1']:
        return 'europe'
    elif server_abbreviation in ['br1', 'la1', 'la2', 'na1']:
        return 'americas'
    elif server_abbreviation in ['jp1', 'kr']:
        return 'asia'
    elif server_abbreviation in ['oc1']:
        return 'sea'
    else:
        return None


def convert(trait, no):
    if trait in ["Set7_Astral", "Set7_Ragewing", "Set7_Jade", "Set7_Legend", "Set7_Dragonmancer"]:
        return no * 3
    elif trait in ["Set7_Whispers", "Set7_Mirage", "Set7_Scalescorn", "Set7_Tempest", "Set7_Swiftshot",
                   "Set7_Assassin", "Set7_Bruiser", "Set7_Cannoneer", "Set7_Guardian", "Set7_Evoker",
                   "Set7_Shapeshifter", "Set7_Warrior", "Set7_Cavalier"]:
        return no * 2
    elif trait in ["Set7_Guild", "Set7_Dragon", "Set7_Spell-Thief", "Set7_Starcaller", "Set7_Bard"]:
        return no
    elif trait in ["Set7_Shimmerscale", "Set7_Mage"]:
        return (no * 2) + 1
    elif trait in ["Set7_Trainer", "Set7_Revel", "Set7_Mystic"]:
        return no + 1
    else:
        return no


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
        except HTTPError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user2 = watcher.summoner.by_name(users_data['server'], users_data['username2'])
        except HTTPError:
            return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        match_list_user1 = watcher.match.by_puuid(convert_server(users_data['server']), user1['puuid'], count=200)
        match_list_user2 = watcher.match.by_puuid(convert_server(users_data['server']), user2['puuid'], count=200)
        common_match_list = list(set(match_list_user1).intersection(match_list_user2))
        if not common_match_list:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        user1_placements, user2_placements, match_lengths = [], [], []
        user1_first, user1_top4, user1_eight, user2_first, user2_top4, user2_eight = 0, 0, 0, 0, 0, 0
        user1_gold_left, user2_gold_left,  = [], []
        user1_less_5_gold, user1_more_20_gold, user2_less_5_gold, user2_more_20_gold = 0, 0, 0, 0
        user1_eliminated_list, user1_max_eliminated, user2_eliminated_list, user2_max_eliminated = [], [], [], []
        user1_total_damage_list, user2_total_damage_list = [], []
        user1_trait_dict, user2_trait_dict = {}, {}
        user1_augment_dict, user2_augment_dict = {}, {}
        user1_items_dict, user2_items_dict = {}, {}
        user1_unit_dict, user2_unit_dict = {}, {}

        for elt in common_match_list:
            game = MatchInfo.game_exists(elt, convert_server(users_data['server']))
            if game:
                match = json.loads(game)
            else:
                match = watcher.match.by_id(convert_server(users_data['server']), elt)
                new_match = {'match_id': str(elt), 'server': str(convert_server(users_data['server'])),
                             'match_data': json.dumps(match), 'created_at': datetime.utcnow()}
                new_match_serializer = MatchInfoSerializer(data=new_match)
                if new_match_serializer.is_valid():
                    new_match_serializer.save()
            match_lengths.append(match['info']['game_length'])
            for participant in match['info']['participants']:
                if participant['puuid'] == user1['puuid']:
                    user1_placements.append(participant['placement'])
                    if participant['placement'] == 1:
                        user1_first += 1
                    if participant['placement'] < 5:
                        user1_top4 += 1
                    if participant['placement'] == 8:
                        user1_eight += 1
                    user1_gold_left.append(participant['gold_left'])
                    if participant['gold_left'] <= 5:
                        user1_less_5_gold += 1
                    elif participant['gold_left'] >= 20:
                        user1_more_20_gold += 1
                    user1_eliminated_list.append(participant['players_eliminated'])
                    user1_max_eliminated.append(8 - int(participant['placement']))
                    user1_total_damage_list.append(participant['total_damage_to_players'])
                    for trait in participant['traits']:
                        if trait['tier_current'] > 0:
                            name = trait['name']
                            tier = convert(name, trait['tier_current'])
                            if name not in user1_trait_dict.keys():
                                user1_trait_dict[name] = {tier: 1}
                            else:
                                if tier not in user1_trait_dict[name].keys():
                                    user1_trait_dict[name][tier] = 1
                                else:
                                    user1_trait_dict[name][tier] += 1
                    for augment in participant['augments']:
                        if augment not in user1_augment_dict.keys():
                            user1_augment_dict[augment] = 1
                        else:
                            user1_augment_dict[augment] += 1
                    for unit in participant['units']:
                        if unit['character_id'] not in user1_unit_dict.keys():
                            user1_unit_dict[unit['character_id']] = 1
                        else:
                            user1_unit_dict[unit['character_id']] += 1
                        for item in unit['itemNames']:
                            if item not in user1_items_dict.keys():
                                user1_items_dict[item] = 1
                            else:
                                user1_items_dict[item] += 1

                if participant['puuid'] == user2['puuid']:
                    user2_placements.append(participant['placement'])
                    if participant['placement'] == 1:
                        user2_first += 1
                    if participant['placement'] < 5:
                        user2_top4 += 1
                    if participant['placement'] == 8:
                        user2_eight += 1
                    user2_gold_left.append(participant['gold_left'])
                    if participant['gold_left'] <= 5:
                        user2_less_5_gold += 1
                    elif participant['gold_left'] >= 20:
                        user2_more_20_gold += 1
                    user2_eliminated_list.append(participant['players_eliminated'])
                    user2_max_eliminated.append(8 - int(participant['placement']))
                    user2_total_damage_list.append(participant['total_damage_to_players'])
                    for trait in participant['traits']:
                        if trait['tier_current'] > 0:
                            name = trait['name']
                            tier = convert(name, trait['tier_current'])
                            if name not in user2_trait_dict.keys():
                                user2_trait_dict[name] = {tier: 1}
                            else:
                                if tier not in user2_trait_dict[name].keys():
                                    user2_trait_dict[name][tier] = 1
                                else:
                                    user2_trait_dict[name][tier] += 1
                    for augment in participant['augments']:
                        if augment not in user2_augment_dict.keys():
                            user2_augment_dict[augment] = 1
                        else:
                            user2_augment_dict[augment] += 1
                    for unit in participant['units']:
                        if unit['character_id'] not in user2_unit_dict.keys():
                            user2_unit_dict[unit['character_id']] = 1
                        else:
                            user2_unit_dict[unit['character_id']] += 1
                        for item in unit['itemNames']:
                            if item not in user2_items_dict.keys():
                                user2_items_dict[item] = 1
                            else:
                                user2_items_dict[item] += 1

        user1_avg = round(mean(user1_placements), 2)
        user2_avg = round(mean(user2_placements), 2)
        user1_eliminated_avg = round(mean(user1_eliminated_list), 2)
        user2_eliminated_avg = round(mean(user2_eliminated_list), 2)
        user1_eliminate_rate = round(mean(user1_eliminated_list) / mean(user1_max_eliminated), 2)
        user2_eliminate_rate = round(mean(user2_eliminated_list) / mean(user2_max_eliminated), 2)
        user1_damage_dealt_avg = round(mean(user1_total_damage_list), 2)
        user2_damage_dealt_avg = round(mean(user2_total_damage_list), 2)
        avg_length = round(mean(match_lengths), 2)
        played_together = len(common_match_list)
        user1_augments = dict(reversed(sorted(user1_augment_dict.items(), key=lambda item: item[1])))
        while len(user1_augments.keys()) > 5:
            del user1_augments[list(user1_augments.keys())[-1]]
        user2_augments = dict(reversed(sorted(user2_augment_dict.items(), key=lambda item: item[1])))
        while len(user2_augments.keys()) > 5:
            del user2_augments[list(user2_augments.keys())[-1]]
        user1_items = dict(reversed(sorted(user1_items_dict.items(), key=lambda item: item[1])))
        while len(user1_items.keys()) > 3:
            del user1_items[list(user1_items.keys())[-1]]
        user2_items = dict(reversed(sorted(user2_items_dict.items(), key=lambda item: item[1])))
        while len(user2_items.keys()) > 3:
            del user2_items[list(user2_items.keys())[-1]]

        # detecting gold lefts
        user1_gold_left_avg = round(mean(user1_gold_left), 2)
        if user1_less_5_gold / played_together >= 0.85:
            if user1_more_20_gold / played_together < 0.1:
                user1_gold_management = "5/5"
            else:
                user1_gold_management = "4/5"
        elif user1_less_5_gold / played_together >= 0.7:
            if user1_more_20_gold / played_together < 0.2:
                user1_gold_management = "4/5"
            else:
                user1_gold_management = "3/5"
        elif user1_less_5_gold / played_together >= 0.55:
            if user1_more_20_gold / played_together < 0.25:
                user1_gold_management = "3/5"
            else:
                user1_gold_management = "2/5"
        elif user1_less_5_gold / played_together >= 0.4:
            if user1_more_20_gold / played_together < 0.15:
                user1_gold_management = "2/5"
            else:
                user1_gold_management = "1/5"
        else:
            user1_gold_management = "1/5"
        user2_gold_left_avg = round(mean(user2_gold_left), 2)
        if user2_less_5_gold / played_together >= 0.85:
            if user2_more_20_gold / played_together < 0.1:
                user2_gold_management = "5/5"
            else:
                user2_gold_management = "4/5"
        elif user2_less_5_gold / played_together >= 0.7:
            if user2_more_20_gold / played_together < 0.2:
                user2_gold_management = "4/5"
            else:
                user2_gold_management = "3/5"
        elif user2_less_5_gold / played_together >= 0.55:
            if user2_more_20_gold / played_together < 0.25:
                user2_gold_management = "3/5"
            else:
                user2_gold_management = "2/5"
        elif user2_less_5_gold / played_together >= 0.4:
            if user2_more_20_gold / played_together < 0.15:
                user2_gold_management = "2/5"
            else:
                user2_gold_management = "1/5"
        else:
            user2_gold_management = "1/5"

        # general info for users
        user1_info = watcher.league.by_summoner(users_data['server'], user1['id'])
        user2_info = watcher.league.by_summoner(users_data['server'], user2['id'])
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
                                'avg_gold_left': user1_gold_left_avg,
                                'gold_management': user1_gold_management,
                                'how_many_eliminated': user1_eliminated_avg,
                                'eliminate_rate': user1_eliminate_rate,
                                'damage_dealt_avg': user1_damage_dealt_avg,
                                'pp': f'https://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/{user1["profileIconId"]}.png',
                                'level': user1['summonerLevel'],
                                'username': users_data['username1'],
                                'units': user1_unit_dict,
                                'traits': user1_trait_dict,
                                'top_augments': user1_augments,
                                'top_items': user1_items},
                         'user2': {
                                'avg': user2_avg,
                                'first': user2_first,
                                'top4': user2_top4,
                                'eight': user2_eight,
                                'league': user2_tier,
                                'points': user2_points,
                                'total_wins': user2_total_wins,
                                'total_losses': user2_total_losses,
                                'avg_gold_left': user2_gold_left_avg,
                                'gold_management': user2_gold_management,
                                'how_many_eliminated': user2_eliminated_avg,
                                'eliminate_rate': user2_eliminate_rate,
                                'damage_dealt_avg': user2_damage_dealt_avg,
                                'pp': f'https://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/{user2["profileIconId"]}.png',
                                'level': user2['summonerLevel'],
                                'username': users_data['username2'],
                                'units': user2_unit_dict,
                                'traits': user2_trait_dict,
                                'top_augments': user2_augments,
                                'top_items': user2_items},
                         'played_together': played_together,
                         'avg_length': avg_length,
                         'created': datetime.now()}
        serializer = UsersComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

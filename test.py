from riotwatcher import TftWatcher

watcher = TftWatcher("RGAPI-2294e978-a22c-4ec1-8efc-17a6ab78fdc6")
user1 = watcher.summoner.by_name("na1", "Dıshsoap")
user2 = watcher.summoner.by_name("na1", "Aesah")
match_list_user1 = watcher.match.by_puuid("americas", user1['puuid'], count=200)
match_list_user2 = watcher.match.by_puuid("americas", user2['puuid'], count=200)
common_match_list = list(set(match_list_user1).intersection(match_list_user2))
print(common_match_list)

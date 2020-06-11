import collections
import json

import requests

# Commands (faceit c) : faceit stats imwos 30

# Best/worst team mate (>x games)
# Best Map KD/Winrate:
# Worst Map KD/Winrate:  e.g: Mirage (0.74KD or 24% winrate)



player_url_request = 'https://open.faceit.com/data/v4/players?nickname=NAME'
match_history_url = 'https://open.faceit.com/data/v4/players/PID/history?game=csgo&offset=0&limit=LIMIT'

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer aed25a75-307b-42c2-b60c-db0886d1381b',
}


#teammate_data_tuple = collections.namedtuple('team_tuple', 'user_id username wins loss kills deaths')
#map_data_tuple = collections.namedtuple('map_tuple', 'count wins kills deaths avg_round_difference')


teammate_map = {s: 0 for s in ''.split()}
map_stats_map = {s: 0 for s in 'count wins kills deaths round_won round_loss'}


def get_player_json(nickname):
    raw_player_json = requests.get(player_url_request.replace('NAME', nickname), headers=headers).content
    return json.loads(raw_player_json)


def get_player_history_json(player_id, limit=20):
    raw_history_json = requests.get(
        match_history_url.replace('PID', player_id).replace('LIMIT', str(limit)), headers=headers).content
    return json.loads(raw_history_json)


def get_match_ids_from_history(history_json: json):
    return [i['match_id'] for i in history_json['items']]


def get_match_json(match_id):
    s = requests.get('https://open.faceit.com/data/v4/matches/MID/stats'.replace('MID', match_id),
                     headers=headers).content
    return json.loads(s)


def merge_map_stats(tally: {}, match: {}) -> {}:
    return {tally[k]+match[k]: v for k, v in tally.items()}


def parse_map_stats(match_json) -> {}:
    r = {}
    round_stats = match_json['rounds']['round_stats']


PlayerStats = collections.namedtuple('PlayerStats', 'user_id username wins loss avg_kills avg_deaths')
MapStats = collections.namedtuple('MapStats', 'count wins kills deaths round_won round_loss')


def get_stats(nickname):
    player_id = get_player_json(nickname)['player_id']
    player_history = get_player_history_json(player_id)
    match_ids = [s['match_id'] for s in player_history['items']]

    map_stat = {}  # Map (Name) -> Statistics  e.g: (Mirage -> {map_stats_map}, ...)

    for match_id in match_ids:

        # Get Match JSON

        # Get statistics for actual player
        #   For each other_player in match_players:
        #
        #
        #
        #

        match_json = get_match_json(match_id)
        t_map = teammate_map.copy()

        map_name = match_json['rounds']['round_stats']['Map']
        #map_tally[map_name] = parse_map_stats(match_json)











x = get_stats('imwos')


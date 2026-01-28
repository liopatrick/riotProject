import requests
from urllib.parse import urlencode
import settings


def get_puuid(game_name=None, tag_line=None, region=settings.DEFAULT_REGION):
    '''
    Wrapper for ACCOUNT-V1 API portal
    Gets player info from SUMMONER based on name
    return Summoner info as dict or none
    '''

    if game_name is None:
        game_name = input('Enter SUMMONER NAME: ')

    if tag_line is None:
        tag_line = input('Enter tagline: ')

    params = {
        'api_key': settings.API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
        '''
        data = response.json()
        puuid = data.get('puuid')
        return puuid
        '''
    except requests.exceptions.RequestException as e:
        print(f"Error getting player info: {e}")
        return None


def get_match_ids(summoner_puuid, matches_count, region=settings.DEFAULT_REGION):
    '''
    get match IDs from summoner

    :param summoner_puuid: Summoner PUUID
    :param matches_count: number of matches to get
    :param region: region where summon is located
    :return: list of match IDs
    '''

    params = {
        'api_key': settings.API_KEY
    }
    api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids")
    # f"?start=0&count={matches_count}")

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting summoner match data from API: {e}")
        return None


def win_check(summoner_puuid, match__id, region=settings.DEFAULT_REGION):
    params = {
        'api_key': settings.API_KEY,
    }
    api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match__id}")

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        match_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting match data from API: {e}")
        return None

    if summoner_puuid in match_data['metadata']['participants']:
        player_index = match_data['metadata']['participants'].index(summoner_puuid)
    else:
        return None

    player_info = match_data['info']['participants'][player_index]
    return player_info['win']


def win_percentage(summoner, tag_line, region=settings.DEFAULT_REGION):
    summoner = get_puuid(summoner, tag_line, region)
    matches = get_match_ids(summoner['puuid'], 20, region)

    wins = 0
    for match in matches:
        if win_check(summoner['puuid'], match):
            wins += 1
    return (wins / len(matches)) * 100


# tft-league-v1
# needs puuid

def league_rank(summoner_puuid, region=settings.DEFAULT_REGION_CODE):
    """
        Gets league rank of summoner

        :param summoner_puuid: Summoner PUUID
        :param region: region where summon is located
        :return: str league rank
    """
    params = {
        'api_key': settings.API_KEY
    }
    api_url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{summoner_puuid}'
    # https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/nLLQW7J5kJSJS7R5fcOPVhgIl4_xTeSK_uplIU5Z5-1GT1rEMCQW1JFHirWnX3bl2tQURV6Ji0gfLA

    rank = ''

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        player_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting match data from API: {e}")
        return None

    for attribute in player_data:
        if attribute['queueType'] == 'RANKED_SOLO_5x5':
            tier = attribute['tier']
            level = attribute['rank']
            rank = tier + " " + level
            break

    if rank == '':
        rank = 'Unranked'

    return rank

def tft_rank(summoner_puuid, region=settings.DEFAULT_REGION_CODE):
    """
        Gets TFT rank of summoner

        :param summoner_puuid: Summoner PUUID
        :param region: region where summon is located
        :return: str tft rank
    """
    params = {
        'api_key': settings.API_KEY
    }
    api_url = f'https://{region}.api.riotgames.com/tft/league/v1/by-puuid/{summoner_puuid}'
    # https://na1.api.riotgames.com/tft/league/v1/by-puuid/nLLQW7J5kJSJS7R5fcOPVhgIl4_xTeSK_uplIU5Z5-1GT1rEMCQW1JFHirWnX3bl2tQURV6Ji0gfLA

    rank = ''

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        player_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting match data from API: {e}")
        return None

    for attribute in player_data:
        if attribute['queueType'] == 'RANKED_TFT':
            tier = attribute['tier']
            level = attribute['rank']
            rank = tier + " " + level
            break

    if rank == '':
        rank = 'Unranked'

    return rank
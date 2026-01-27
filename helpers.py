import requests
from urllib.parse import urlencode
import settings

def get_puuid(game_name=None, tag_line=None, region = settings.DEFAULT_REGION):
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

def get_match_ids(summoner_puuid, matches_count, region = settings.DEFAULT_REGION):
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
                #f"?start=0&count={matches_count}")

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting summoner match data from API: {e}")
        return None

def win_check(summoner_puuid, match__id, region = settings.DEFAULT_REGION):
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

def win_percentage(summoner, tag_line, region = settings.DEFAULT_REGION):
    summoner = get_puuid(summoner, tag_line, region)
    matches = get_match_ids(summoner['puuid'], 20, region)

    wins = 0
    for match in matches:
        if win_check(summoner['puuid'], match):
            print('win')
            wins += 1
        else:
            print('loss')
    return (wins/len(matches))*100
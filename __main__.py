from helpers import get_puuid, get_match_ids, win_check, win_percentage

game_name = "umihi"
tag_line = "G2B"

summoner = get_puuid(game_name, tag_line)
print(summoner)

summoner_matches = get_match_ids(summoner['puuid'], 20)
print(summoner_matches)

win = win_check(summoner['puuid'], summoner_matches[0])
print(win)

win_ratio = win_percentage(game_name, tag_line)
print(win_ratio)

#https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/umihi/G2B?api_key=RGAPI-3259592f-2b2e-4aed-9a3b-4dac32a7ed60
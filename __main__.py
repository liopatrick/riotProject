from helpers import get_puuid, get_match_ids, win_check, win_percentage, league_rank, tft_rank
import sys


def main(args):
    if len(args) != 1:
        print("Usage: python3 __main__.py <name#tag>")
        return

    if "#" not in sys.argv[1]:
        print("Usage: python3 __main__.py <name#tag> no hash")
        return

    riot_user = sys.argv[1].split("#")

    game_name = riot_user[0]
    tag_line = riot_user[1]

    summoner = get_puuid(game_name, tag_line)

    '''
    # summoner_matches = get_match_ids(summoner['puuid'], 20)
    # win = win_check(summoner['puuid'], summoner_matches[0])
    # win_ratio = win_percentage(game_name, tag_line)
    '''

    summoner_rank_lol = league_rank(summoner['puuid'])
    print("League rank: " + summoner_rank_lol)

    summoner_rank_tft = tft_rank(summoner['puuid'])
    print("TFT rank: " + summoner_rank_tft)

    # https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/umihi/G2B?api_key=RGAPI-3259592f-2b2e-4aed-9a3b-4dac32a7ed60


if __name__ == "__main__":
    main(sys.argv[1:])

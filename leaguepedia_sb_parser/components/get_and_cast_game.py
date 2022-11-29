from bayesapiwrapper import BayesApiWrapper
import riot_transmute
from riotwatcher import LolWatcher
import os
import json


def get_bayes_game(game):
    summary, details = BayesApiWrapper().get_game(game)
    game_dto = cast_game(summary, details)
    return game_dto


def get_riot_api_key():
    config_path = os.path.join(os.path.expanduser("~"), ".config", "leaguepedia_sb_parser")
    keys_file = os.path.join(config_path, "keys.json")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.isfile(keys_file):
        print("The Riot API Key was not found")
        riot_api_key = input("Riot API key: ")
        with open(file=keys_file, mode="w+", encoding="utf8") as f:
            json.dump(
                {"riot_api_key": riot_api_key}, f, ensure_ascii=False
            )
    with open(file=keys_file, mode="r+", encoding="utf8") as f:
        riot_api_key = json.load(f)["riot_api_key"]
    return riot_api_key


def get_live_game(game):
    lol_watcher = LolWatcher(get_riot_api_key())
    region = game.split("_")[0]
    summary, details = lol_watcher.match.by_id(
        region, game
    ), lol_watcher.match.timeline_by_match(region, game)
    game_dto = cast_game(summary["info"], details["info"])
    return game_dto


def cast_game(game_summary, game_details):
    game_dto_summary = riot_transmute.v5.match_to_game(game_summary)
    game_dto_details = riot_transmute.v5.match_timeline_to_game(game_details)
    merged_dto = riot_transmute.merge_games_from_riot_match_and_timeline(
        game_dto_summary, game_dto_details
    )
    return merged_dto

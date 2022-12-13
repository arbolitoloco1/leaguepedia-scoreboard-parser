from bayesapiwrapper import BayesApiWrapper
import riot_transmute
from riotwatcher import LolWatcher
import os


def get_bayes_game(game):
    summary, details = BayesApiWrapper().get_game(game)
    game_dto = cast_game(summary, details)
    return game_dto


def get_live_game(game):
    lol_watcher = LolWatcher(os.environ.get("RIOT_API_KEY"))
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

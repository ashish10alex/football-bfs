import os
import pandas as pd
from typing import List, Dict

from flask import Flask, render_template, request
from fuzzywuzzy import process

from bfs import bfs
from teams_crest_dict import teams_crest_dict
from player_names_to_id_mapping import player_names_to_id_mapping

api_key = os.environ.get("FOOTBALL_API_KEY")

all_teams = list(teams_crest_dict.keys())

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        req = request.form
        player_one, player_two = req["PlayerOne"], req["PlayerTwo"]
        player_one = 'L. Messi'
        connection_result_list = bfs(player_one, player_two)
        print(f"connection_result_list  : {connection_result_list}")
        teams = get_team_names_from_connection_result_list(connection_result_list)
        players = get_player_names_from_connection_result_list(connection_result_list)
        print(f"teams: {teams}")
        print(f"players: {players}")
        image_paths_players = get_image_paths_from_player_names(players)
        print(f"image_paths_players: {image_paths_players}")
        crest_url_dict = crest_url_dict_given_team_names(teams)
        print(f"crest_url_dict : {crest_url_dict }")
        new_connection_resuls_list = get_new_connection_results_list(
            connection_result_list, crest_url_dict
        )
        print(f"new_connection_resuls_list : {new_connection_resuls_list }")
        return render_template(
            "index.html",
            connection_result_list=new_connection_resuls_list,
            teams_crest_dict=teams_crest_dict,
            image_paths_players=image_paths_players,
        )


def get_images():
    headers = {"X-Auth-Token": api_key}
    url = "http://api.football-data.org/v2/teams"
    teams_data = requests.get(url, headers=headers)
    return teams_data


def get_player_id(player_name: str) -> int:
    return player_names_to_id_mapping[player_name]


def get_image_paths_from_player_names(players: List[str]) -> dict:
    df = pd.read_csv("data/player_teams_played_for_mmapping.csv")
    player_image_urls = {}
    for player in players:
        player_pic_url = df[df['player_name'] == player]['player_pics'].values[0]
        player_image_urls[player] = player_pic_url
    return player_image_urls


def fuzzy_match(team_name: str) -> str:
    match = process.extractOne(str(team_name), all_teams)
    return match


def get_team_names_from_connection_result_list(
    connection_result_list: List[str],
) -> List[str]:
    teams = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 != 0:
            teams.append(item)
    return teams


def get_player_names_from_connection_result_list(
    connection_result_list: List[str],
) -> List[str]:
    players = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 == 0:
            players.append(item)
    return players


def get_new_connection_results_list(
    connection_result_list: List[str], crest_url_dict: Dict[str, str]
) -> List[str]:
    new_teams_keys = list(crest_url_dict.keys())[::-1]
    new_connection_result_list = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 != 0:
            new_connection_result_list.append(new_teams_keys.pop())
        else:
            new_connection_result_list.append(item)
    return new_connection_result_list


def crest_url_dict_given_team_names(teams: List[str]) -> Dict[str, str]:
    crest_url_dict = {}
    for team_name in teams:
        key = fuzzy_match(team_name)[0]
        crest_url_dict[key] = teams_crest_dict[str(key)]
    return crest_url_dict


if __name__ == "__main__":
    app.run(debug=True, port=5050)

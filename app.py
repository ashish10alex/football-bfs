import os
import requests
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
        player_one = 'L. Messi' #hardcode Messi
        connection_result_list = bfs(player_one, player_two)
        connection_result_list = [item.strip(' ') for item in connection_result_list]
        print(f"connection_result_list  : {connection_result_list}")

        teams = get_team_names_from_connection_result_list(connection_result_list)

        players = get_player_names_from_connection_result_list(connection_result_list)
        print(f"teams: {teams}")
        print(f"players: {players}")

        player_image_paths = get_image_paths_from_player_names(players)
        print(f"image_paths_players: {player_image_paths}")

        crest_url_dict = crest_url_dict_given_team_names(teams)
        print(f"crest_url_dict : {crest_url_dict }")

        new_connection_resuls_list = get_new_connection_results_list(
            connection_result_list, crest_url_dict
        )

        print(f"new_connection_resuls_list : {new_connection_resuls_list }")
        return render_template(
            "index.html",
            connection_result_list=new_connection_resuls_list,
            teams_crest_dict=crest_url_dict,
            player_image_paths=player_image_paths,
        )


def download_and_save_player_image(image_url:str, player_id:int, img_path='static/player_images/') -> str:
    img_data = requests.get(image_url).content
    img_path = img_path + str(player_id) + '.png'
    with open(img_path, 'wb') as handler:
        handler.write(img_data)
    return img_path

def download_and_save_player_national_team_flag(image_url:str, player_team:str, img_path='static/player_images/') -> str:
    img_data = requests.get(image_url).content
    player_team = player_team.replace(' ', '_')
    img_path = img_path + str(player_team) + '.png'
    with open(img_path, 'wb') as handler:
        handler.write(img_data)
    return img_path


def get_image_paths_from_player_names(players: List[str]) -> dict:
    df = pd.read_csv("data/player_teams_played_for_mmapping.csv")
    player_image_paths = {}
    for player in players:
        player_pic_url = df[df['player_name'] == player]['player_pics'].values[0]
        player_id = df[df['player_name'] == player]['player_id'].values[0]

        # check if img_path already exists
        img_path = 'static/player_images/' + str(player_id) + '.png'
        if os.path.exists(img_path):
            player_image_paths[player] = img_path
        else:
            image_path = download_and_save_player_image(player_pic_url, player_id)
            player_image_paths[player] = image_path

    return player_image_paths


def fuzzy_match(team_name: str):
    match = process.extractOne(str(team_name), all_teams)
    return match


def get_team_names_from_connection_result_list( connection_result_list: list) -> list:
    teams = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 != 0:
            teams.append(item)
    return teams


def get_player_names_from_connection_result_list( connection_result_list: List[str]) -> List[str]:
    players = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 == 0:
            players.append(item)
    return players


def get_new_connection_results_list( connection_result_list: List[str], crest_url_dict: Dict[str, str]) -> List[str]:
    new_teams_keys = list(crest_url_dict.keys())[::-1]
    new_connection_result_list = []
    for idx, item in enumerate(connection_result_list):
        if idx % 2 != 0:
            new_connection_result_list.append(new_teams_keys.pop())
        else:
            new_connection_result_list.append(item)
    return new_connection_result_list


def crest_url_dict_given_team_names(teams: List[str]) -> Dict[str, str]:
    df = pd.read_csv("data/FIFA22_official_data.csv")
    crest_url_dict = {}
    for team in teams:
        if team in df["Club"].values:
            crest_url = df[df["Club"] == team]["Club Logo"].values[0]
            crest_url_dict[team] = download_and_save_player_national_team_flag(crest_url, team)
        else:
            crest_url = df[df['Nationality'] == team ].Flag.iloc[0]
            crest_url_dict[team] = download_and_save_player_national_team_flag(crest_url, team)
    return crest_url_dict


if __name__ == "__main__":
    app.run(debug=True, port=5050)

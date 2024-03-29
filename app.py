import os
import requests
import pandas as pd
import duckdb as db
from typing import List, Dict
from termcolor import colored

from flask import Flask, render_template, request
from fuzzywuzzy import process
from youtubesearchpython import VideosSearch

from bfs import bfs

app = Flask(__name__)
messi_goals = "data/messi_goals.parquet"
fifa_22_data = "data/FIFA22_official_data.parquet"

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        req = request.form
        reference_player, player_two = req["PlayerOne"], req["PlayerTwo"]
        reference_player = 'L. Messi' #hardcode Messi

        print(f'reference_player {reference_player}')
        print(f'player_two {player_two}')

        connection_result_list = bfs(reference_player, player_two)
        connection_result_list = [item.strip(' ') for item in connection_result_list]
        print(f"connection_result_list  : {connection_result_list}")

        teams = get_team_names_from_connection_result_list(connection_result_list)

        players = get_player_names_from_connection_result_list(connection_result_list)
        print(f"teams: {teams}")
        print(f"players: {players}")


        keeper_stats_vs_player =  get_keeper_stats_vs_player(players[:-1], reference_player)
        print(f"keeper_stats_vs_player: {keeper_stats_vs_player}")

        video_id_dict = get_video_ids_from_players(keeper_stats_vs_player, reference_player)
        print(f"video_id_dict: {video_id_dict}")

        player_image_paths = get_image_paths_from_player_names(players)
        print(f"image_paths_players: {player_image_paths}")

        crest_url_dict = crest_url_dict_given_team_names(teams)
        print(f"crest_url_dict : {crest_url_dict }")

        return render_template(
            "index.html",
            connection_result_list=connection_result_list,
            teams_crest_dict=crest_url_dict,
            player_image_paths=player_image_paths,
            keeper_stats_vs_player=keeper_stats_vs_player,
            video_id_dict = video_id_dict
        )


@app.route("/stats", methods=["GET", "POST"])
def kepper_stats_vs_reference_player():

    if request.method == "GET":
        return render_template("keeper_stats.html")

    if request.method == "POST":
        req = request.form
        _, goal_keeper = req["PlayerOne"], req["PlayerTwo"]
        reference_player = 'L. Messi' #hardcode Messi


        player_image_paths = get_image_paths_from_player_names([goal_keeper])
        print(f"image_paths_players: {player_image_paths}")

        # TODO: get team crest for goal keeper
        # crest_url_dict = crest_url_dict_given_team_names(player_teams)
        # print(f"crest_url_dict : {crest_url_dict }")

        keeper_stats_vs_player =  get_keeper_stats_vs_player([goal_keeper], reference_player)

        if len(keeper_stats_vs_player) != 0:
            competitions = keeper_stats_vs_player[goal_keeper]['Comp'].to_list()
            goals = keeper_stats_vs_player[goal_keeper]['goals'].to_list()
            keeper_club = keeper_stats_vs_player[goal_keeper]['Opponent'].to_list()
        else:
            competitions, goals = [], []

        return render_template(
            "keeper_stats.html",
            player_image_paths = player_image_paths,
            keeper_stats_vs_player = keeper_stats_vs_player,
            competitions = competitions,
            goals = goals,
            keeper_club = keeper_club,
        )

def get_video_ids_from_players(final_keeper_dict: dict, reference_player:str) -> dict:
    video_id_dict = {}
    for keeper, stats in final_keeper_dict.items():
        if len(stats['Comp'] ) > 0:
            video_id_dict[keeper] = VideosSearch(query=f'{reference_player} vs {keeper} {stats["Comp"][0]} {stats["Opponent"][0]} goal', limit=1, ).result()['result'][0]['id']
        else: video_id_dict[keeper] = ''
    return video_id_dict

def get_keeper_stats_vs_player(keepers: List[str], reference_player: str) -> dict:
    df = pd.read_parquet(messi_goals)
    goals_stats_keeper_by_reference_player = {}
    for keeper in keepers:
        fuzzy_matched_player, matching_confidence = fuzzy_match_player(keeper)
        if matching_confidence > 75:
            goals_by_competition = db.query(f"select Comp, Opponent , count(*) as goals from df where Goalkeeper = '{fuzzy_matched_player}' group by Comp, Opponent ").to_df()
            goals_by_competition.reset_index(drop=True, inplace=True)
            print(f'goals_by_competition {goals_by_competition}')
            goals_stats_keeper_by_reference_player[keeper] = goals_by_competition.to_dict('list')
        else:
            print(f'Matched {keeper} as {fuzzy_matched_player} with confidence {matching_confidence}, creating empty dataframe')
            goals_stats_keeper_by_reference_player[keeper] = pd.DataFrame(columns=['Comp', 'Opponent', 'goals']).to_dict('list')
    return goals_stats_keeper_by_reference_player


def download_and_save_player_image(image_url:str, player_id:int, img_path='static/player_images/') -> str:
    img_data = requests.get(image_url).content
    img_path = img_path + str(player_id) + '.png'
    with open(img_path, 'wb') as handler:
        handler.write(img_data)
    return img_path



def get_image_paths_from_player_names(players: List[str]) -> dict:
    df = pd.read_parquet("data/player_teams_played_for_mapping.parquet")
    player_image_paths = {}
    for player in players:
        player_pic_url = df[df['player_name'] == player]['player_pics'].values[0]
        player_id = df[df['player_name'] == player].index[0]

        # check if img_path already exists
        img_path = 'static/player_images/' + str(player_id) + '.png'
        if os.path.exists(img_path):
            player_image_paths[player] = img_path
        else:
            print(colored(f"Downloading image for {player}", 'red'))
            image_path = download_and_save_player_image(player_pic_url, player_id)
            player_image_paths[player] = image_path

    return player_image_paths


def fuzzy_match_player(player: str) -> tuple[str, int]:
    df = pd.read_parquet(messi_goals)
    players = df['Goalkeeper'].values
    fuzzy_matched_player, matching_confidence = process.extractOne(str(player), players)
    return fuzzy_matched_player, matching_confidence

def fuzzy_match_team(team: str) -> tuple[str, int]:
    df = pd.read_parquet(fifa_22_data)
    teams = df['Club'].values
    fuzzy_matched_team, matching_confidence = process.extractOne(str(team), teams)
    return fuzzy_matched_team, matching_confidence


def get_team_names_from_connection_result_list(connection_result_list: List[str]) -> List[str]:
    # every odd index is a team name
    teams = [connection_result_list[idx] for idx in range(len(connection_result_list)) if idx % 2 != 0 ]
    return teams


def get_player_names_from_connection_result_list(connection_result_list: List[str]) -> List[str]:
    # every even index is a player name
    players = [connection_result_list[idx] for idx in range(len(connection_result_list)) if idx % 2 == 0 ]
    return players

def download_and_save_player_national_team_flag(image_url:str, player_team:str, img_path='static/player_images/') -> str:
    player_team = player_team.replace(' ', '_')
    img_path = img_path + str(player_team) + '.png'
    if os.path.exists(img_path):
        return img_path
    print(colored(f"Downloading image for {player_team}", 'red'))
    img_data = requests.get(image_url).content
    with open(img_path, 'wb') as handler:
        handler.write(img_data)
    return img_path

def check_if_team_is_club_or_national_team_and_return_crest(team: str, df:pd.DataFrame) -> str:
    df = df.copy()
    if team in df["Club"].values:
        crest_url = df[df["Club"] == team]["Club Logo"].values[0]
        return download_and_save_player_national_team_flag(crest_url, team)
    elif team in df["Nationality"].values:
        crest_url = df[df['Nationality'] == team ].Flag.iloc[0]
        return download_and_save_player_national_team_flag(crest_url, team)


def crest_url_dict_given_team_names(teams: List[str]) -> Dict[str, str]:
    df = pd.read_parquet(fifa_22_data)
    crest_url_dict = {}
    for team in teams:
        if team in df["Club"].values or team in df["Nationality"].values:
            crest_url_dict[team] = check_if_team_is_club_or_national_team_and_return_crest(team, df)
        else:
            fuzzy_matched_team, matching_confidence = fuzzy_match_team(team)
            print(f"team: {fuzzy_matched_team} matched with {matching_confidence} confidence")
            crest_url_dict[team] = check_if_team_is_club_or_national_team_and_return_crest(fuzzy_matched_team, df)
    return crest_url_dict

if __name__ == "__main__":
    app.run(debug=True)

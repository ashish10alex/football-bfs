import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pdbr

df = pd.read_csv("data/FIFA22_official_data.csv")
print(len(df))

player_ids = list(df["ID"])

player_urls = []
for player_id in player_ids:
    player_url = f"https://sofifa.com/player/{player_id}/live"
    player_urls.append(player_url)
df["player_urls"] = player_urls


def get_teams_player_played_for(player_url, idx):
    page_html = requests.get(player_url).content
    page_html_soup = BeautifulSoup(page_html, "html.parser")
    teams_table = page_html_soup.find_all(class_="text-ellipsis")

    # for all items in teams_table that has class team, get the td element
    teams = []
    for team in teams_table:
        if team.find(class_="team"):
            team_name = team.text
            teams.append(team_name)
    teams = set(teams)
    return df["Name"][idx], df["ID"][idx], list(teams)

# parallel computation using threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for idx, url in tqdm(enumerate(player_urls[:])):
        results.append(executor.submit(get_teams_player_played_for, url, idx))
    final_results = []
    for f in concurrent.futures.as_completed(results):
        final_results.append(f.result())

df_player_teams = pd.DataFrame(columns=["player", "teams"])

player_ids = []
player_names = []
player_teams = []
for data in final_results:
    player_name, player_id, teams = data
    player_ids.append(player_id)
    player_names.append(player_name)
    player_teams.append(teams)

df_player_teams["player_id"] = player_ids
df_player_teams["player_name"] = player_names
df_player_teams["teams"] = player_teams

df_player_teams.to_pickle("data/player_teams_played_for_mmapping.pkl")
df_player_teams.to_csv("data/player_teams_played_for_mmapping.csv", index=False)

# idx = 11
# df_small.iloc[idx]['player'], df_small.iloc[idx]['teams']

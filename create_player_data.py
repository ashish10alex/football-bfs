import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pdbr

df = pd.read_csv("data/FIFA22_official_data.csv")
print(len(df))

#extract position from dataframe
df['Position'] = df['Position'].str.split('>', 1).str[-1]

#filter for messi and goalkeepers only
df = df[(df['Position']=='GK') | (df['ID'] == 158023)] 
df.reset_index(inplace=True)


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
    return df["Name"][idx], df["ID"][idx], df["Photo"][idx], list(teams)

# get_teams_player_played_for(player_urls[0], 0)

# parallel computation using threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for idx, url in tqdm(enumerate(player_urls[:])):
        results.append(executor.submit(get_teams_player_played_for, url, idx))
    final_results = []
    for f in concurrent.futures.as_completed(results):
        final_results.append(f.result())

df_player_teams = pd.DataFrame(columns=["teams"])

player_ids = []
player_names = []
player_pics = []
player_teams = []
for data in final_results:
    player_name, player_id, player_pic, teams = data
    player_ids.append(player_id)
    player_names.append(player_name)
    player_pics.append(player_pic)
    player_teams.append(teams)

df_player_teams["player_id"] = player_ids
df_player_teams["player_name"] = player_names
df_player_teams["teams"] = player_teams
df_player_teams["player_pics"] = player_pics

df_player_teams.to_csv("data/player_teams_played_for_mapping.csv", index=False, encoding="utf-8")

# idx = 11
# df_small.iloc[idx]['player'], df_small.iloc[idx]['teams']

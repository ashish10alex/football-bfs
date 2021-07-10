import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

df = pd.read_csv("data/players_20.csv")

player_urls = list(df["player_url"])

player_urls_new = []

for url in player_urls:
    new_url = "/".join(url.split("/")[:-2]) + "/live"
    player_urls_new.append(new_url)
df["player_urls_new"] = player_urls_new


def get_teams_player_played_for(player_url, idx):
    page_html = requests.get(player_url).content
    page_html_soup = BeautifulSoup(page_html, "html.parser")
    teams_table = page_html_soup.find_all(class_="team")
    teams = set()
    for item in teams_table[2:]:
        teams.add(item.text)
    return df["long_name"][idx], list(teams)


# test get_teams_player_played_for function
# idx = 11
# result= get_teams_player_played_for(df['player_urls_new'][idx], idx)
# result

# sequential
# player_teams_played_for = []
# for idx, url in tqdm(enumerate(player_urls_new[:30])):
#     teams = get_teams_player_played_for(url, idx)
#     player_teams_played_for.append(teams)
# df['player_teams_played_for'] =  player_teams_played_for

# parallel computation using threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for idx, url in tqdm(enumerate(player_urls_new[:800])):
        results.append(executor.submit(get_teams_player_played_for, url, idx))
    final_results = []
    for f in concurrent.futures.as_completed(results):
        final_results.append(f.result())

df_small = pd.DataFrame(columns=["player", "teams"])

player_names = []
player_teams = []
for data in final_results:
    player_name, teams = data
    player_names.append(player_name)
    player_teams.append(teams)

df_small["player"] = player_names
df_small["teams"] = player_teams
df_small.to_pickle("data/data_small.pkl")
df_small.to_csv("data/data_small.csv")

# idx = 11
# df_small.iloc[idx]['player'], df_small.iloc[idx]['teams']

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


df["player_urls"] = [f"https://sofifa.com/player/{player_id}" for player_id in df["ID"]]

def get_teams_player_played_for(player_url, idx):
    page_html = requests.get(player_url).content
    soup = BeautifulSoup(page_html, "html.parser")
    table_rows = soup.find_all("tr")
    player_teams = set([row.find('a').text for row in table_rows if row.find('img', {'class': 'team', 'data-type': 'team'})])
    return idx, player_teams

# un comment for testing
# get_teams_player_played_for(df['player_urls'][0], 0)

df_player_teams = pd.DataFrame(columns=["idx",  "player_name", "player_pics", "teams"])

# parallel computation using threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for idx, url in df['player_urls'][:].items():
        results.append(executor.submit(get_teams_player_played_for, url, idx))
    idxs = []
    player_teams = []
    for f in concurrent.futures.as_completed(results):
        idxs.append(f.result()[0])
        player_teams.append(f.result()[1])



df_player_teams["idx"] = idxs
df_player_teams["teams"] = player_teams

df_player_teams.set_index("idx", inplace=True)

df_player_teams['player_pics'] = df.iloc[df_player_teams.index]['Photo']
df_player_teams['player_name'] = df.iloc[df_player_teams.index]['Name']


df_player_teams.to_csv("data/player_teams_played_for_mapping_test.csv", index=True, encoding="utf-8")

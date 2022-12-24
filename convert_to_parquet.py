import pandas as pd
import pyarrow.parquet as pq

#convert dataframe to parquet
def convert_to_parquet(filenames):
    for filename in filenames:
        df = pd.read_csv(filename)
        filename = filename.replace('.csv', '.parquet')
        df.to_parquet(filename, engine='pyarrow')



filenames = ['data/messi_goals.csv', 'data/player_teams_played_for_mapping.csv', 'data/FIFA22_official_data.csv']
convert_to_parquet(filenames)


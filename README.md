
## Football BFS


Shows the shortest connection between Messi and a Goalkeeper


<!-- <img width="700" alt="football_bfs_tree" src="https://user-images.githubusercontent.com/34306898/208472128-bc3f5936-6a86-485f-aacc-8937f16a9496.png"> -->


![foo](https://user-images.githubusercontent.com/34306898/208893256-4db177c8-2855-489b-9a26-de8597549476.gif)



This project is my attempt at a football version of - [Oracle of bacon](https://oracleofbacon.org/movielinks.php) 



 Website also shows number of goals Messi has scored on a goal keeper across various competitions

<img width="600" alt="football_stats" src="https://user-images.githubusercontent.com/34306898/208269586-0ca92a35-b229-4a95-a81b-1acb636b47df.png">


Shows the shortest connection between Messi and a Goalkeeper

#### Development setup

Tested on Python 3.10.8

Create virtual environment 
```
python3 -m venv messi
source messi/bin/activate
```

Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

Run web app
```
python app.py

# For football tree go to - 
`http://127.0.0.1:5050`

# For stats go to - 
`http://127.0.0.1:5050/stats`
```

`create_player_data.py` - Parses urls to extract information of clubs that a football player has belonged to
Breadth first search code borrowed from - https://github.com/a8hay/kevin-bacon-bfs

API dashboard - https://dashboard.api-football.com/

#### TODOs -

- [ ] Make website faster - 
    - Use Parquet file format instead of csv for faster loading [<b style='color:green'> done </b>]
    - Donot load dataframe multiple times
    - Do not over use fuzzy matching
- [ ] Expand across other players than Messi. That is make the reference player dynamic 
- [x] Embed youtube video of latest goal vs goal keeper
- [ ] Better error handling 
- [ ] Testing sripts
- [ ] Create an ETL pipeline to update data dynamically
- [ ] Move player vs detailed stats to another branch
- [x] Get pictures of players from "data/FIFA22_official_data.csv"


#### Known bugs -
- Might require multiple refreshes to show connections for some players. 
- Need to update dataset to have more correct info on what clubs / national teams a player played for

### Dataset credits w/t links

1. [Messi goals](https://fbref.com/en/players/d70ce98e/goallogs/all_comps/Lionel-Messi-Goal-Log#goallogs_goals)
2. [Which player played for what club / national team](https://sofifa.com/)
2. [Player photo and national team crests](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset)



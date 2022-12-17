
## Football BFS


Shows the shortest connection between Messi and a Goalkeeper

<img width="400" alt="football_tree" src="https://user-images.githubusercontent.com/34306898/128848361-de01367f-07af-4ec1-a3fc-99a9e1fff439.png">

This eventually plans to be a football version of - https://oracleofbacon.org/movielinks.php

`localhost/stats` will show number of goals Messi has scored on a goal keeper across various competitions

<img width="400" alt="football_stats" src="https://user-images.githubusercontent.com/34306898/128848361-de01367f-07af-4ec1-a3fc-99a9e1fff439.png">

Shows the shortest connection between Messi and a Goalkeeper

Run -
```
pip3 -r requirements.txt
python app.py
```

`create_player_data.py` - Parses urls to extract information of clubs that a football player has belonged to
Breadth first search code borrowed from - https://github.com/a8hay/kevin-bacon-bfs

API dashboard - https://dashboard.api-football.com/

TODOs -

- [ ] Make BFS file faster
- [x] Get pictures of players from "data/FIFA22_official_data.csv"
- [x] Try another API - https://www.api-football.com/news (maybe no need for API anymore)

Known bugs -~


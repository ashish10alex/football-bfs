
## Football BFS


Shows the graph between two players indicating the shortest connection between them 
E.g connection between between players

```
Virgil van Dijk -->Liverpool -->Mohamed  Salah Ghaly -->Chelsea -->N'Golo Kanté

Paul Pogba -->Manchester United -->Gerard Piqué Bernabéu -->Barcelona -->Lionel Andrés Messi Cuccittini

Lionel Andrés Messi Cuccittini -->Barcelona -->Miralem Pjanić -->Juventus -->Cristiano Ronaldo dos Santos Aveiro
```
<img width="400" alt="football_tree" src="https://user-images.githubusercontent.com/34306898/128848361-de01367f-07af-4ec1-a3fc-99a9e1fff439.png">

This eventually plans to be a football version of - https://oracleofbacon.org/movielinks.php

Run -
```
python app.py
```

`create_player_data.py` - Parses urls to extract information of clubs that a football player has belonged to
Breadth first search code borrowed from - https://github.com/a8hay/kevin-bacon-bfs

API dashboard - https://dashboard.api-football.com/

TODOs -

- [ ] Make virtualenv for this project
- [ ] Get pictures of players from "data/FIFA22_official_data.csv"
- [ ] Check the correctness of current bfs implementation as the results are randomly off sometimes
- [ ] Make bfs file faster
- [x] Try another API - https://www.api-football.com/news (maybe no need for API anymore)

Bugs -
- [ ] Sometimes doesn't show the correct links - fixes on adding a breakpoint in `bfs.py` and continuing from the
    breakpoint
- [ ] Generated data using web scraping has some missing values in players, repeated entries e.g. `'Monaco II', 'Monaco'`.  API tried (https://www.football-data.org) free tier doesn't list squad. 


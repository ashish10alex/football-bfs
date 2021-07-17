## Football BFS


Shows the graph between two players indicating the shortest connection between them 
E.g connection between between players

```
Virgil van Dijk -->Liverpool -->Mohamed  Salah Ghaly -->Chelsea -->N'Golo Kanté

Paul Pogba -->Manchester United -->Gerard Piqué Bernabéu -->Barcelona -->Lionel Andrés Messi Cuccittini

Lionel Andrés Messi Cuccittini -->Barcelona -->Miralem Pjanić -->Juventus -->Cristiano Ronaldo dos Santos Aveiro
```

This eventually plans to be a football version of - https://oracleofbacon.org/movielinks.php

Run -
```
python app.py
```

`create_player_data.py` - Parses urls to extract information of clubs that a football player has belonged to
Breadth first search code borrowed from - https://github.com/a8hay/kevin-bacon-bfs

TODOs -

- [ ] Get pictures of players of all top 5 leagues
- [ ] Check the correctness of current bfs implementation
- [x] Try another API - https://www.api-football.com/news
- [ ] Make bfs file faster

Bugs -
- [ ] Generated data using web scraping has some missing values in players, repeated entries e.g. `'Monaco II', 'Monaco'`.  API tried (https://www.football-data.org) free tier doesn't list squad. 
- [ ] Sometimes doesn't show the correct links 


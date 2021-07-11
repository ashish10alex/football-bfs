## Football BFS


Shows the graph between two players indicating the shortest connection between them 
E.g connection between Virgil van Dijk and N'Golo Kanté 

`Virgil van Dijk -->Liverpool -->Mohamed  Salah Ghaly -->Chelsea -->N'Golo Kanté`

Another example - 
`Paul Pogba -->Manchester United -->Gerard Piqué Bernabéu -->Barcelona -->Lionel Andrés Messi Cuccittini`

This eventually plans to be a football version of - https://oracleofbacon.org/movielinks.php

Run -
```
python bfs.py
```

`create_player_data.py` - Parses urls to extract information of clubs that a football player has belonged to
Breadth first search code borrowed from - https://github.com/a8hay/kevin-bacon-bfs

TODOs -

* Check the correctness of current bfs implementation
* Web interface for player selection
* Fuzzy search player name (fzf?)
* Bugs -
  - Generated data using web scraping has some missing values in players, repeated entries e.g. `'Monaco II', 'Monaco'`.  API tried (https://www.football-data.org) free tier doesnt list squad. Could be used to get other info such as logos

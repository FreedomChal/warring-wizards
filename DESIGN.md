# warring-wizards Design

Warring Wizards uses the Flask web server when run locally, but uses Gunicorn instead to improve performance when run on Heroku.
  
The underlying functionality of Warring Wizards is primarily based on three entity classes: User, Game, and Player. Each entity type also has a table in database.db associated with it. 

* User stores information about the user, and is used for identification and authentication.
* Game stores information about games, such as whether the game is running and its available slots.
* Player stores information about in-game players. It stores stats such as health, and also references both its User and the Game it is in.

Most functionality in the app is based on these three entities. Each one also has sub-entities such as Repositories, which are used to get entities from the database.

Regarding Users, each user has permissions. Currently, there are two permissions: can_create_games and is_administrator. Both of these default to false, and can only be changed by manually changing the database.
Players for which can_create_games is false are not allowed to create games.
is_administrator currently doesn't do anything.

The game itself uses the flask-socketio library. Each game has its own room, corresponding to the game id, which is used for managing comminication in a single game. The updates sent through sockets from client to server are:

* A request for update. The server will then get the stats of the current player from the database, as well as the timestamp of when the player was last updated. The server will then calculate the difference between the current timestamp and the timestamp from the last update, and grow the player's stats accordingly. The server will then update the database, and send stat data back to the client, as well as to all other players in the game so that they can see the player's health and level.
* A message to attack. When the player attacks another player, it will tell the server what player the are attacking. The server will then get the stats of both players, and inflict damage on the victim based on the attacker's energy and strength, as well as deplete the attacker's energy. If the victim has nonpositive health, they are then set to dead, and an update is sent to the client. If the victim is killed, the server will check if the game is done, and if it is, it will archive the game and notify the winner that they have won.
* A message to upgrade. When upgrading a stat, the stat to be upgraded and the amount to upgrade will be sent to the server. If the amount is negative, the server will ignore the update. If the amount is valid, the server will get the player's stats from the database, and then upgrade the desired stat by the amount specified. If the specified amount is more than the player can afford, it will upgrade by the highest amount the player can afford.
* In the waiting room, the client will periodically check if the game has started. When the client checks, the server will both check whether the game has no more player slots and whether the waiting time has passed. If either are true, it will notify all clients in the game that the game has started, and all players will be redirected to their game.

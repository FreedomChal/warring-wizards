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

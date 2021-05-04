CREATE TABLE players (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	game_id INTEGER,
	hp REAL,
	max_hp REAL,
	heal REAL,
	armor REAL,
	attack REAL,
	income INTEGER,
	coins INTEGER,
	energy REAL,
	energy_increase REAL,
	energy_acceleration REAL,
	FOREIGN KEY (user_id)
		REFERENCES users (id),
	FOREIGN KEY (game_id)
		REFERENCES games(id)
);

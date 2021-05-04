DROP table players;

CREATE TABLE players (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id REAL,
	game_id REAL,
	hp REAL,
	max_hp REAL,
	heal REAL,
	armor REAL,
	attack REAL,
	income REAL,
	coins REAL,
	energy REAL,
	energy_increase REAL,
	energy_acceleration REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id)
		REFERENCES users (id),
	FOREIGN KEY (game_id)
		REFERENCES games(id)
);

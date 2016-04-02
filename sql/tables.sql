CREATE TABLE users(
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(30) NOT NULL UNIQUE,
	password VARCHAR(200) NOT NULL,
	email VARCHAR(50) UNIQUE DEFAULT null,
	profile_image VARCHAR(300),
	email_verified BOOLEAN DEFAULT false,
	gcm_id TEXT,
	PRIMARY KEY(id)
);

CREATE TABLE events( 
	id INT NOT NULL AUTO_INCREMENT, 
	name VARCHAR(30) NOT NULL,
	info VARCHAR(500) NOT NULL,
	image VARCHAR(70) NOT NULL,
	location VARCHAR(30) NOT NULL, 
	start_time TIMESTAMP NOT NULL, 
	end_time TIMESTAMP NOT NULL,
	match_card VARCHAR(500) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE messages(
	id INT NOT NULL AUTO_INCREMENT,
	event_id INT NOT NULL,
	user_id INT NOT NULL,
	body VARCHAR(250) NOT NULL,
	FOREIGN KEY (event_id) REFERENCES events(id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
);

INSERT INTO users(username, email, password) VALUES ("JaySyko", "jay@jaysyko.com", "password");

INSERT INTO events(name, info, image, location, start_time, end_time, match_card) 
VALUES ("Monday Night RAW", "A 3 Hour Shit Show","Mpk5lUg.jpg","Toronto, Ontario", now(), now(), "TBA");

INSERT INTO messages(event_ID, user_id, body) VALUES ((SELECT id FROM events WHERE id = 1), (SELECT id FROM users WHERE id = 1), 'LMFAOO for real!?');
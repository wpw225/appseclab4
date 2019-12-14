CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(64), 
	password_hash VARCHAR(128), 
	password2_hash VARCHAR(128), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_username ON user (username);
CREATE TABLE login (
	id INTEGER NOT NULL, 
	login_timestamp DATETIME, 
	logout_timestamp DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE INDEX ix_login_login_timestamp ON login (login_timestamp);
CREATE INDEX ix_login_logout_timestamp ON login (logout_timestamp);
CREATE TABLE post (
	id INTEGER NOT NULL, 
	body VARCHAR(1000), 
	timestamp DATETIME, 
	user_id INTEGER, 
	result VARCHAR(1000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE INDEX ix_post_timestamp ON post (timestamp);

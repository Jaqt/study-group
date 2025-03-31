CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    group_name TEXT,
    description TEXT,
    max_members INTEGER,
    subject TEXT,
    owner INTEGER REFERENCES users
);

CREATE TABLE users_groups(
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);
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
    owner INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE users_groups(
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    group_id INTEGER REFERENCES groups ON DELETE CASCADE
);

CREATE TABLE messages(
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    group_id INTEGER REFERENCES groups ON DELETE CASCADE,
    message TEXT,
    time TEXT
);

CREATE INDEX idx_groups_owner ON groups(owner);
CREATE INDEX idx_users_groups_group ON users_groups(group_id);
CREATE INDEX idx_users_groups_user_group ON users_groups(user_id, group_id);
CREATE INDEX idx_messages_group_time ON messages(group_id, time DESC);
CREATE INDEX idx_messages_user_time ON messages(user_id, time DESC);

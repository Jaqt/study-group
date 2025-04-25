import db

from werkzeug.security import generate_password_hash, check_password_hash

# Create user
def create_user(username, password):
    if check_username(username):
        return False
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    return db.execute(sql, [username, password_hash])

# Checks if username already exists before inserting into db
def check_username(username):
    sql = "SELECT username FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None

# Check login credentials
def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

# Get username by id
def get_user(user_id):
    sql = "SELECT users.id, users.username FROM users WHERE users.id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

# Get groups user is the owner/founder of
def get_owner(user_id):
    sql = """SELECT groups.id, groups.group_name
            FROM groups
            WHERE groups.owner = ?"""
    return db.query(sql, [user_id])

# Get groups which user is currently member of
def get_groups(user_id):
    sql = """SELECT groups.id, groups.group_name
            FROM groups, users_groups
            WHERE users_groups.user_id = ?
            AND groups.id = users_groups.group_id"""
    return db.query(sql, [user_id])

# Get subjects of the groups user is part of
def get_subjects(user_id):
    sql = """SELECT groups.subject, COUNT(*)
            FROM groups, users_groups
            WHERE users_groups.user_id = ? AND users_groups.group_id = groups.id
            GROUP BY groups.subject"""
    return db.query(sql, [user_id])
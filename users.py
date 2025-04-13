import db

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
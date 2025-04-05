import db

# Listing of all groups in db
def get_groups():
    sql = "SELECT id, group_name, description, subject FROM groups ORDER BY id DESC"
    return db.query(sql)

# Get group page
def get_group(group_id):
    sql = """SELECT groups.group_name,
                    groups.description,
                    groups.max_members,
                    groups.subject,
                    groups.owner,
                    groups.id
            FROM groups
            WHERE groups.id = ?"""
    group_data = db.query(sql, [group_id])[0]

    sql = """SELECT users.username
            FROM users, users_groups
            WHERE users.id = users_groups.user_id
            AND users_groups.group_id = ?"""
    members = db.query(sql, [group_id])
    return group_data, members

# Create a group to db
def create_group(group_name, description, max_members, subject, user_id):
    sql = """INSERT INTO groups (group_name, description, max_members, subject, owner)
            VALUES (?, ?, ?, ?, ?)"""
    group_id = db.execute(sql, [group_name, description, max_members, subject, user_id])
    add_member(user_id, group_id)

# add member to a group
def add_member(user_id, group_id):
    sql = "INSERT INTO users_groups (user_id, group_id) VALUES (?, ?)"
    db.execute(sql, [user_id, group_id])

# update group
def update_group(group_id, group_name, description, max_members, subject):
    sql = """UPDATE groups SET group_name = ?,
                               description = ?,
                               max_members = ?,
                               subject = ?
                            WHERE id = ?"""
    db.execute(sql, [group_name, description, max_members, subject, group_id])

# delete group
def delete_group(group_id):
    sql = "DELETE FROM groups WHERE groups.id = ?"
    db.execute(sql, [group_id])
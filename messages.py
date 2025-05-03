import db

# get messages for the group
def get_messages(group_id):
    sql = """SELECT messages.id AS message_id,
                    users.id AS user_id,
                    users.username,
                    messages.message,
                    messages.time
             FROM messages, users
             WHERE messages.user_id = users.id AND messages.group_id = ?
             ORDER BY messages.id DESC"""
    return db.query(sql, [group_id])

# insert message into db
def new_message(user_id, group_id, message):
    sql = """INSERT INTO messages (user_id, group_id, message, time) VALUES
             (?, ?, ?, datetime('now'))"""
    db.execute(sql, [user_id, group_id, message])
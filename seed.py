import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM groups")
db.execute("DELETE FROM users_groups")
db.execute("DELETE FROM messages")

USER_COUNT = 1000
GROUP_COUNT = 10**6
MESSAGE_COUNT = 10**7

for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, GROUP_COUNT + 1):
    subjects = ["tira", "tikape", "linis", "lama"]
    subject = random.choice(subjects)
    db.execute("""INSERT INTO groups (group_name,
                                    description,
                                    max_members,
                                    subject,
                                    owner)
                VALUES (?, ?, ?, ?, ?)""",
               ["group" + str(i), "test", random.randint(1, 32), subject, random.randint(1, 32)])

for i in range(1, MESSAGE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    group_id = random.randint(1, GROUP_COUNT)
    db.execute("""INSERT INTO messages (user_id, group_id, message, time)
                  VALUES (?, ?, ?, datetime('now'))""",
               [user_id, group_id, "message" + str(i)])

db.commit()
db.close()

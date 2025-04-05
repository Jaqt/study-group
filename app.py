import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import groups

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords don't match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: account name is already taken"

    return "Account created"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "ERROR: wrong username or password"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "GET":
        return render_template("create_group.html")

    if request.method == "POST":
        group_name = request.form["group_name"]
        description = request.form["description"]
        max_members = request.form["max_members"]
        subject = request.form["subject"]

        groups.create_group(group_name, description, max_members, subject, session["user_id"])

        return redirect("/")
    
@app.route("/update_group", methods=["POST"])
def update_group():
    group_id = request.form["group_id"]
    group_name = request.form["group_name"]
    description = request.form["description"]
    max_members = request.form["max_members"]
    subject = request.form["subject"]

    groups.update_group(group_id, group_name, description, max_members, subject)

    return redirect("/view/group_id=" + str(group_id))

@app.route("/delete_group", methods=["POST"])
def delete_group():
    group_id = request.form["group_id"]
    if "delete" in request.form:
        groups.delete_group(group_id)
        return redirect("/")
    
    return redirect("/view/group_id=" + str(group_id))

@app.route("/groups")
def list_groups():
    all_groups = groups.get_groups()
    return render_template("/groups.html", groups = all_groups)

@app.route("/view/group_id=<int:group_id>")
def view_group(group_id):
    group_data, members = groups.get_group(group_id)
    return render_template("group_page.html", group = group_data, members = members)

@app.route("/edit/group_id=<int:group_id>")
def edit_group(group_id):
    group_data, members = groups.get_group(group_id)
    return render_template("edit_group.html", group = group_data, members = members)

@app.route("/delete/group_id=<int:group_id>")
def remove_group(group_id):
    return render_template("delete_group.html", group_id=group_id)
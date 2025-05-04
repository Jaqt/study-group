import secrets
import math
from functools import wraps

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import markupsafe

import config
import db
import groups
import users
import messages

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to be logged in to access this page", "warning")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    my_groups = None
    if "user_id" in session:
        my_groups = users.get_groups(session["user_id"])
    return render_template("index.html", groups=my_groups)

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    if not username or len(username) > 16:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not password1 or len(password1) > 128:
        abort(403)
    if password1 != password2:
        flash("Passwords don't match", "warning")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    if not users.create_user(username, password1):
        flash("Username is already taken", "warning")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    flash("Account creation successful, log in.", "success")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            abort(403)
        password = request.form["password"]
        if not password or len(password) > 128:
            abort(403)

        user_id = users.check_login(username, password)
        if not user_id:
            flash("Wrong username or password", "warning")
            return render_template("login.html")

        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
        del session["csrf_token"]
    return redirect("/")

@app.route("/groups")
@app.route("/groups/<int:page>")
def list_groups(page=1):
    page_size = 10
    group_count = groups.group_count()
    page_count = math.ceil(group_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/groups/1")
    if page > page_count:
        return redirect("/groups/" + str(page_count))

    all_groups = groups.get_groups(page, page_size)
    return render_template("/groups.html", groups=all_groups, page=page, page_count=page_count)

@app.route("/search_group")
def search_group():
    query = request.args.get("query")
    if not query:
        return redirect("/groups/1")
    filter_groups = groups.filter_groups(query)
    return render_template("/groups.html", groups=filter_groups, query=query)

@app.route("/create_group", methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "GET":
        return render_template("create_group.html")

    if request.method == "POST":
        check_csrf()
        group_name = request.form["group_name"]
        if not group_name or len(group_name) > 50:
            abort(403)
        description = request.form["description"]
        if not description or len(description) > 1000:
            abort(403)
        max_members = request.form["max_members"]
        if not max_members or int(max_members) < 1 or int(max_members) > 32:
            abort(403)
        subject = request.form["subject"]
        if not groups.valid_subjects(subject):
            abort(403)

        groups.create_group(group_name, description, max_members, subject, session["user_id"])
        group_id = db.last_insert_id()
        groups.add_member(session["user_id"], group_id)

        return redirect("/view/group_id=" + str(group_id))

@app.route("/update_group", methods=["POST"])
@login_required
def update_group():
    check_csrf()

    group_id = request.form["group_id"]
    group = groups.get_group(group_id)
    if not group:
        abort(404)
    if group["owner"] != session["user_id"]:
        abort(403)

    group_name = request.form["group_name"]
    if not group_name or len(group_name) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    max_members = request.form["max_members"]
    if not max_members or int(max_members) < 1 or int(max_members) > 32:
        abort(403)
    subject = request.form["subject"]
    if not groups.valid_subjects(subject):
        abort(403)

    if "cancel" in request.form:
        return redirect("/view/group_id=" + str(group_id))

    groups.update_group(group_id, group_name, description, max_members, subject)

    flash("Group information has been updated", "success")
    return redirect("/view/group_id=" + str(group_id))

@app.route("/delete_group", methods=["POST"])
@login_required
def delete_group():
    check_csrf()

    group_id = request.form["group_id"]
    group = groups.get_group(group_id)
    if not group:
        abort(404)
    if group["owner"] != session["user_id"]:
        abort(403)

    if "delete" in request.form:
        groups.delete_group(group_id)
        flash("Group has been successfully deleted", "success")
        return redirect("/")

    return redirect("/view/group_id=" + str(group_id))

@app.route("/new_message", methods=["POST"])
@login_required
def new_message():
    check_csrf()

    group_id = int(request.form["group_id"])
    if not group_id:
        abort(403)
    message = request.form["message"].strip()
    if not message or len(message) > 140:
        abort(403)

    members = groups.get_members(group_id)
    is_member = False
    for member in members:
        if session["user_id"] == member[0]:
            is_member = True

    if not is_member:
        abort(403)

    messages.new_message(session["user_id"], group_id, message)

    return redirect("/view/group_id=" + str(group_id))

@app.route("/join_group/group_id=<int:group_id>", methods=["POST"])
@login_required
def join_group(group_id):
    check_csrf()

    group_data = groups.get_group(group_id)
    if not group_data:
        abort(404)

    members = groups.get_members(group_id)
    for member in members:
        if session["user_id"] == member[0]:
            flash("You have already joined this group", "warning")
            return redirect("/view/group_id=" + str(group_id))

    if len(members) >= group_data["max_members"]:
        flash("This group is full!", "warning")
        return redirect("/view/group_id=" + str(group_id))

    groups.add_member(session["user_id"], group_id)
    flash("You have joined the group", "success")
    return redirect("/view/group_id=" + str(group_id))

@app.route("/leave_group/group_id=<int:group_id>", methods=["POST"])
@login_required
def leave_group(group_id):
    check_csrf()

    group_data = groups.get_group(group_id)
    if not group_data:
        abort(404)
    if group_data["owner"] == session["user_id"]:
        abort(403)

    members = groups.get_members(group_id)
    for member in members:
        if session["user_id"] == member[0]:
            groups.remove_member(session["user_id"], group_id)
            flash("You have left the group", "success")
            return redirect("/view/group_id=" + str(group_id))

    abort(403)

@app.route("/view/group_id=<int:group_id>")
@login_required
def view_group(group_id):
    group_data = groups.get_group(group_id)
    if not group_data:
        abort(404)

    members = groups.get_members(group_id)
    is_member = False
    for member in members:
        if session["user_id"] == member[0]:
            is_member = True
    group_messages = messages.get_messages(group_id)
    is_full = len(members) >= group_data["max_members"]
    return render_template("group_page.html", group=group_data, members=members,
                           group_messages=group_messages, is_member=is_member,
                           is_full=is_full)

@app.route("/edit/group_id=<int:group_id>")
@login_required
def edit_group(group_id):
    group_data = groups.get_group(group_id)
    if not group_data:
        abort(404)
    if group_data["owner"] != session["user_id"]:
        abort(403)
    return render_template("edit_group.html", group=group_data)

@app.route("/delete/group_id=<int:group_id>")
@login_required
def remove_group(group_id):
    group_data = groups.get_group(group_id)
    if not group_data:
        abort(404)
    if group_data["owner"] != session["user_id"]:
        abort(403)
    return render_template("delete_group.html", group_id=group_id)

@app.route("/view/user_id=<int:user_id>")
@login_required
def view_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    group_messages = messages.users_messages(user_id)
    owner = users.get_owner(user_id)
    users_groups = users.get_groups(user_id)
    subjects = users.get_subjects(user_id)
    return render_template("user_page.html", user=user, group_messages=group_messages,
                           owner=owner, users_groups=users_groups, subjects=subjects)

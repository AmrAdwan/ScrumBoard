from flask import Flask, flash, redirect, render_template, g, request, session, url_for
import manage_users as ma_us
import manage_tickets as ma_ti
import database_handler2 as db_handler
from enums import status, rights
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

dbHandler = db_handler.DbHandler()
manageUsers = ma_us.ManageUsers(dbHandler)
manageTickets = ma_ti.ManageTickets(dbHandler, manageUsers)

@app.before_request
def before_request():
    g.user_authenticated = check_user_authentication()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/board')
def board():
    columns = ['Backlog', 'Ready', 'In Progress', 'Review', 'Done']
    colors = ['danger', 'warning', 'info', 'secondary', 'success']
    combined = zip(columns, colors)
    valid_users = manageUsers.getUsersByRights(rights.DRAG)
    column_tickets = manageTickets.get_tickets_by_column(columns)
    active_user = manageUsers.active_user
    return render_template('board.html', combined=list(combined), valid_users=valid_users, column_tickets=column_tickets, active_user=active_user)

@app.route('/add_task', methods=["POST"])
def add_task():
    if request.method == "POST":
        result = request.form
        create_success = manageTickets.create_ticket(result["title"], result["description"], status.BACKLOG, result["hours"])
        if create_success and int(result["assignee"]) != -1:
            user_success = manageTickets.add_user_to_ticket(manageUsers.get_user(int(result["assignee"])), manageTickets.get_ticket(title=result["title"]))
    return board()

@app.route('/del_task', methods=["POST"])
def del_task():
    if request.method == "POST":
        result = request.form
        remove_success = manageTickets.remove_ticket(manageTickets.get_ticket(int(result["ticket_id"])))
    return board()

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/manage_users')
def manage_users():
    if not session.get('user_authenticated') or session.get('user_rights') != 6:
        return redirect(url_for('board'))

    # Retrieve and pass user data to the template
    users =  manageUsers.users
    return render_template('manage_users.html', users=users)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form
        # print(result)
        valid_info = manageUsers.login(result["userName"], result["password"])
        if valid_info:
            session['user_authenticated'] = True
            # Assigning user rights after successful login
            session['user_rights'] = manageUsers.get_active_user_rights()
            session["username"] = result["userName"]
            return redirect(url_for("board"))
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        valid_info = manageUsers.register_user(result["userName"], result["password1"], result["password2"])
        if valid_info:
            return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/home')
def logout():
    manageUsers.logout()
    return redirect(url_for("home"))

@app.route('/upload_img')
def upload_img():
    return render_template('upload_img.html')

@app.route('/set_profile_picture', methods=["POST"])
def set_profile_picture():
    if request.method == 'POST':
        img = request.files['img']
        if img.filename == '':
            return redirect(url_for("home"))
        if manageUsers.active_user is None:
            return redirect(url_for("home"))
        manageUsers.change_user_picture(img)
    return redirect(url_for("home"))

def check_user_authentication():
    if manageUsers.active_user is not None:
        return True
    return False  


@app.route('/user/<int:user_id>/change_rights', methods=["GET", "POST"])
def change_user_rights(user_id):
    user = manageUsers.get_user(user_id=user_id)
    if not user:
        return "User not found", 404

    if request.method == "POST":
        if 'rights' in request.form:
            new_rights = int(request.form['rights'])
            if manageUsers.change_user_rights(user_id, new_rights):
                return redirect(url_for('manage_users'))
            else:
                logging.error(f"Failed to update rights for user {user_id}")
                return "Failed to update rights", 400

    return render_template('change_user_rights.html', user=user, rights=list(rights))


@app.route('/user/<int:user_id>/reset_password', methods=["GET", "POST"])
def reset_user_password(user_id):
    user = manageUsers.get_user(user_id=user_id)
    if not user:
        return "User not found", 404

    if request.method == "POST":
        if 'password' not in request.form:
            return "Password field is missing.", 400
        new_password = request.form['password']
        if manageUsers.change_user_password(new_password, user):
            return redirect(url_for('manage_users'))
        else:
            return "Failed to reset password", 400

    return render_template('reset_user_password.html', user=user)


@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if manageUsers.remove_user(user_id):
        # When successful deletion
        return redirect(url_for('manage_users'))
    else:
        # Handle failure case
        return "Error deleting user", 400
    

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        print(password, "  ", confirm_password)
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('create_user'))

        if manageUsers.register_user(username, password, confirm_password, "", False):
            flash('User created successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash('Failed to create user.', 'error')
            return redirect(url_for('create_user'))
    
    return render_template('create_user.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
from flask import Flask, redirect, render_template, g, request, session, url_for
import manage_users as ma_us
import manage_tickets as ma_ti
import database_handler2 as db_handler
from enums import status, rights
import os

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

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form
        # print(result)
        valid_info = manageUsers.login(result["userName"], result["password"])
        if valid_info:
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

def check_user_authentication():
    if manageUsers.active_user != None:
        return True
    return False  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
from flask import Flask, redirect, render_template, g, request, url_for
import manage_users as ma_us
import manage_tickets as ma_ti
import database_handler2 as db_handler

app = Flask(__name__)

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
    return render_template('board.html', combined=list(combined))


@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form
        valid_info = manageUsers.login(result["userName"], result["password"])
        if valid_info:
            return render_template('board.html')
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        valid_info = manageUsers.register_user(result["userName"], result["password1"], result["password2"])
        if valid_info:
            return render_template('login.html')
    return render_template('register.html')

def check_user_authentication():
    return False  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

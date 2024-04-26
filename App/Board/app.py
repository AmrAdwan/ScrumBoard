import base64
import re
from flask import Flask, flash, jsonify, redirect, render_template, g, request, session, url_for
import manage_users as ma_us
import manage_tickets as ma_ti
import database_handler2 as db_handler
from enums import status, rights
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}




dbHandler = db_handler.DbHandler()
manageUsers = ma_us.ManageUsers(dbHandler)
manageTickets = ma_ti.ManageTickets(dbHandler, manageUsers)

@app.context_processor
def inject_db_handler():
    return dict(dbHandler=dbHandler)


@app.before_request
def before_request():
    g.user_authenticated = 'user_id' in session and session.get('user_authenticated', False)

    
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."

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
    active_ticket = manageTickets.get_ticket(1)#manageTickets.active_ticket
    if active_user is None:
        return redirect(url_for('home'))
    else:
        return render_template('board.html', combined=list(combined), valid_users=valid_users, column_tickets=column_tickets,
                           active_user=active_user, tickets=manageTickets.tickets)

@app.route('/add_task', methods=["POST"])
def add_task():
    if request.method == "POST":
        result = request.form
        create_success = manageTickets.create_ticket(result["title"], result["description"], status.BACKLOG, result["hours"])
        if create_success and int(result["assignee"]) != -1:
            user_success = manageTickets.add_user_to_ticket(manageUsers.get_user(int(result["assignee"])), manageTickets.get_ticket(title=result["title"]))
    return redirect(url_for('board'))

@app.route('/del_task', methods=["POST", "GET"])
def del_task():
    if request.method == "POST":
        result = request.form
        remove_success = manageTickets.remove_ticket(manageTickets.get_ticket(int(result["ticket_id"])))
    return redirect(url_for('board'))

@app.route('/edit_task', methods=["POST", "GET"])
def edit_task():
    if request.method == "POST":
        result = request.form
        ticket = manageTickets.get_ticket(int(result["ticket_id"]))
        ava_edit = {"title": False, "description": False, "status": False, "hours": False, "users": False}
        if "edit_field" in result:
            ava_edit[result["edit_field"]] = True
        elif "edit_field" in result:
            ava_edit[result["edit_field"]] = True
        return render_template('edit_task.html', ticket=ticket, ava_edit=ava_edit, status=status, users=manageUsers.get_free_users(ticket))
    return redirect(url_for('board'))

@app.route('/update_task', methods=["POST", "GET"])
def update_task():
    if request.method == "POST":
        result = request.form
        ticket = manageTickets.get_ticket(int(result["ticket_id"]))
        manageTickets.edit_ticket(ticket,
                                  result["title"] if "title" in result else None,
                                  result["description"] if "description" in result else None,
                                  status[result["status"]] if "status" in result else None,
                                  result["hours"] if "hours" in result else None)
        ava_edit = {"title": False, "description": False, "status": False, "hours": False, "users": False}
        return render_template('edit_task.html', ticket=ticket, ava_edit=ava_edit, status=status, users=manageUsers.get_free_users(ticket))
    return redirect(url_for("home"))

@app.route('/add_user_ticket', methods=["POST", "GET"])
def add_user_ticket():
    if request.method == "POST":
        result = request.form
        user = manageUsers.get_user(int(result["user_id"]))
        ticket = manageTickets.get_ticket(int(result["ticket_id"]))
        manageTickets.add_user_to_ticket(user, ticket)
        ava_edit = {"title": False, "description": False, "status": False, "hours": False, "users": True}
        return render_template('edit_task.html', ticket=ticket, ava_edit=ava_edit, status=status, users=manageUsers.get_free_users(ticket))
    return redirect(url_for("home"))

@app.route('/del_user_ticket', methods=["POST", "GET"])
def del_user_ticket():
    if request.method == "POST":
        result = request.form
        user = manageUsers.get_user(int(result["user_id"]))
        ticket = manageTickets.get_ticket(int(result["ticket_id"]))
        manageTickets.remove_user_from_ticket(user, ticket)
        ava_edit = {"title": False, "description": False, "status": False, "hours": False, "users": True}
        return render_template('edit_task.html', ticket=ticket, ava_edit=ava_edit, status=status, users=manageUsers.get_free_users(ticket))
    return redirect(url_for("home"))

@app.route('/account', methods=['GET', 'POST'])
def account():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not found', 'error')
        return redirect(url_for('login'))

    user = manageUsers.get_user(user_id=user_id)
    if not user:
        return "User not found", 404

    if request.method == "POST":
        result = request.form
        oldPassword = result.get('oldPassword')
        newPassword = result.get('ChangePassword')
        confNewPassword = result.get('confChangePassword')

        if not oldPassword:
            flash('Old password required!', 'error')
            return render_template('account.html')

        elif not newPassword:
            flash('New password required!', 'error')
            return render_template('account.html')
        
        elif not confNewPassword:
            flash('Confirm new password required!', 'error')
            return render_template('account.html')
        
        elif newPassword != confNewPassword:
            flash('New password and its confirmation should be the same', 'error')
            return render_template('account.html')

        is_valid, message = validate_password(newPassword)
        if not is_valid:
            flash(message, 'error')
            return render_template('account.html')

        # Verify the old password is correct
        if not dbHandler.check_username_password(user.username, user.user_id, oldPassword):
            flash('Old password is incorrect', 'error')
            return render_template('account.html')

        # If old password is correct, update to the new password
        valid_info = manageUsers.change_user_password(newPassword, user)
        if valid_info:
            flash('Password updated successfully!', 'success')
            return redirect(url_for("home"))
        else:
            flash('Failed to update password.', 'error')
    only_admin = None
    for user in manageUsers.users:
        if manageUsers.check_only_admin(user):
            only_admin = user

    return render_template('account.html', only_admin=only_admin)




@app.route('/manage_users')
def manage_users():
    user_rights = session.get('user_rights')
    if not session.get('user_authenticated') or session.get('user_rights') != 6:
        flash('Insufficient rights to access this page.', 'error')
        return redirect(url_for('board'))

    # Retrieve and pass user data to the template
    users = manageUsers.users
    only_admin = None
    for user in users:
        if manageUsers.check_only_admin(user):
            only_admin = user
    return render_template('manage_users.html', users=users, only_admin=only_admin)

@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = manageUsers.get_user(user_id=session['user_id'])
        return {'user': user}
    return {}


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form

        if not result['userName']:
            flash('User Name is required!', 'error')
        elif not result['password']:
            flash('Password is required!', 'error')

        valid_info, user_id = manageUsers.login(result["userName"], result["password"])
        if valid_info:
            session['user_authenticated'] = True
            session['user_id'] = user_id
            session['user_rights'] = manageUsers.get_active_user_rights()
            session["username"] = result["userName"]
            
            img_data = dbHandler.get_profile_picture(user_id)
            # print("imgggggg::: ", img_data)
            if img_data:
                img_filename = f'user_{user_id}.png'
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
                try:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                    session['user_profile_pic'] = img_filename
                    # print("image:::: " , img_filename)
                except Exception as e:
                    print(f"Failed to write image file: {e}")
                    flash('Failed to save profile picture.', 'error')
            
            return redirect(url_for("board"))
        else:
            if result['userName'] and result['password']:
                flash('Login failed, please check your username and password.', 'error')
    return render_template('login.html')




@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form

        if not result['userName']:
            flash('User Name is required!', 'error')
            return render_template('register.html')

        if not result['password1'] or not result['password2']:
            flash('Password and password confirmation are required!', 'error')
            return render_template('register.html')

        if result['password1'] != result['password2']:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        is_valid, message = validate_password(result['password1'])
        if not is_valid:
            flash(message, 'error')
            return render_template('register.html')

        valid_info = manageUsers.register_user(result["userName"], result["password1"], result["password2"])
        if valid_info:
            flash('User registered successfully!', 'success')
            return redirect(url_for("login"))
        else:
            flash('Failed to register user.', 'error')

    return render_template('register.html')

@app.route('/home')
def logout():
    manageUsers.logout()
    session.pop('user_id', None) 
    session.pop('user_authenticated', None)
    session.clear()

    # Remove user_id from session
    session['user_authenticated'] = False
    return redirect(url_for("home"))

@app.route('/upload_img')
def upload_img():
    return render_template('upload_img.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/set_profile_picture', methods=["POST"])
def set_profile_picture():
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for("login"))
        
    user_id = session['user_id']
    img = request.files.get('img')
    
    if img and allowed_file(img.filename):
        filename = secure_filename(img.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(filepath)
        
        # Update the database
        with open(filepath, "rb") as img_file:
            manageUsers.change_user_picture(img_file, user_id)
            flash("Profile picture updated successfully!", "success")
        
        # Update the session
        with open(filepath, "rb") as img_file:
            img_data = img_file.read()
            encoded_img_data = base64.b64encode(img_data).decode('utf-8')
            session['user_profile_pic'] = encoded_img_data

        flash("Profile picture updated successfully!", "success")
    else:
        flash("Failed to update profile picture", "error")
        
    return redirect(url_for("account"))



# @app.route('/user/<int:user_id>/change_rights', methods=["GET", "POST"])
# def change_user_rights(user_id):
#     if not session.get('user_authenticated') or session.get('user_rights') != 6:
#         return redirect(url_for('home'))

#     user = manageUsers.get_user(user_id=user_id)
#     if not user:
#         return "User not found", 404

#     if request.method == "POST":
#         if 'rights' in request.form:
#             new_rights = int(request.form['rights'])
#             if manageUsers.change_user_rights(user_id, new_rights):
#                 return redirect(url_for('manage_users'))
#             else:
#                 logging.error(f"Failed to update rights for user {user_id}")
#                 return "Failed to update rights", 400

#     return render_template('change_user_rights.html', user=user, rights=list(rights))

@app.route('/user/<int:user_id>/change_rights', methods=["GET", "POST"])
def change_user_rights(user_id):
    if not session.get('user_authenticated') or session.get('user_rights') != 6:
        flash('Insufficient rights to access this page.', 'error')
        return redirect(url_for('home'))

    user = manageUsers.get_user(user_id=user_id)
    if not user:
        flash('User not found', 'error')
        return "User not found", 404

    if request.method == "POST":
        if 'rights' in request.form:
            new_rights = int(request.form['rights'])
            if manageUsers.change_user_rights(user_id, new_rights):
                # If the current user's rights were changed, update the session
                if user_id == session.get('user_id'):
                    session['user_rights'] = new_rights
                    # If the rights are no longer admin, log the user out
                    if new_rights != 6:
                        flash('Your rights have been updated. Please log in again.', 'info')
                        return redirect(url_for('logout'))
                flash('User rights updated successfully!', 'success')
                return redirect(url_for('manage_users'))
            else:
                flash('Failed to update rights.', 'error')
                return "Failed to update rights", 400

    return render_template('change_user_rights.html', user=user, rights=list(rights))




@app.route('/user/<int:user_id>/reset_password', methods=["GET", "POST"])
def reset_user_password(user_id):
    if not session.get('user_authenticated') or session.get('user_rights') != 6:
        return redirect(url_for('home'))
    user = manageUsers.get_user(user_id=user_id)
    if not user:
        return "User not found", 404

    if request.method == "POST":
        new_password = request.form.get('password', '')
        
        if not new_password:
            flash('Password is required!', 'error')
            return render_template('reset_user_password.html', user=user)

        is_valid, message = validate_password(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('reset_user_password.html', user=user)

        if manageUsers.change_user_password(new_password, user):
            flash('Password reset successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash('Failed to reset password.', 'error')

    return render_template('reset_user_password.html', user=user)


@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if manageUsers.active_user is None:
        return redirect(url_for('home'))
    active_id = manageUsers.active_user.user_id
    if manageUsers.remove_user(user_id):
        # When successful deletion
        if active_id == user_id:
            return redirect(url_for('logout'))
        else:
            return redirect(url_for('manage_users'))
    else:
        # Handle failure case
        return "Error deleting user", 400


@app.route('/delete_account', methods=["POST", "GET"])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        flash('No user authenticated', 'error')
        return redirect(url_for('login'))

    if manageUsers.remove_user(user_id):
        session.pop('user_id', None)
        session.pop('user_authenticated', None)
        session.clear()
        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('home'))
    else:
        flash('Failed to delete account.', 'error')
        return redirect(url_for('account'))

    
@app.route('/update_ticket_status', methods=['POST'])
def update_ticket_status():
    # The request JSON contains 'ticket_id' and 'new_status'
    data = request.json
    print("dataaaa: " , data)
    ticket_id = data.get('ticket_id')
    new_status = data.get('new_status')
    # print("new_status:    " + new_status)

    # Fetch the ticket object using the ticket_id
    ticket = manageTickets.get_ticket(ticket_id=ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404

    try:
        # Convert the new status to the enum type
        new_status_enum = status[new_status.upper()]
    except KeyError:
        return jsonify({'error': 'Invalid status'}), 400

    # Call the change_ticket_status method
    if manageTickets.change_ticket_status(ticket=ticket, status=new_status_enum):
        return jsonify({'success': 'Ticket status updated'}), 200
    else:
        return jsonify({'error': 'Failed to update ticket status'}), 500
    

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('create_user'))

        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
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

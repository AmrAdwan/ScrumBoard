from flask import Flask, redirect, render_template, g, request, url_for

app = Flask(__name__)

@app.before_request
def before_request():
    g.user_authenticated = check_user_authentication()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
      pass
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
      pass
    return render_template('register.html')

def check_user_authentication():
    return False  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "Elliot"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/Sign_up', methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
    #   username = request.form.get("username")
    #   password = request.form.get("password")
            user = Users(username=request.form.get("username"), password=request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            number = 3
            while number >= 0:
                time.sleep(1)
                number -= 1
                if number == 0:
                    return redirect(url_for("login"))
        else:
            return render_template("Sign_up.html")
    except:
        return f"username " + user.username + " and/or " + user.password + " already exists"


@app.route("/log_in", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return render_template("welcome.html")
    else:
        return render_template("log_in.html")


@app.route("/log_out")
def logout():
    logout_user()
    return redirect(url_for("log_in"))


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

app.run(port= 5000, debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import check_password_hash, generate_password_hash
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registrations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "registrations.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------ MODEL ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.Text)

# ------------------ main ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    users = User.query.all()
    return render_template("home.html", users=users)

# ------------------ register ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        comment = request.form.get("comment")
        # ------------------ validation ------------------
        existing = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first() #get first existing user in to existing variable either through email or username or none

        if existing:
            flash("User already exists", "danger")
            return redirect(url_for("register"))
        # ------------------ storing in database ------------------
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            comment=comment
        )

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["username"] = user.username

        return redirect(url_for("dashboard"))  # ✅ FIX

    return render_template("register.html")


# ------------------ Login ------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier")  # username or email
        password = request.form.get("password")

        user = User.query.filter((User.username == identifier) | (User.email == identifier) ).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect username/email or password.", "danger")
            return redirect(url_for("login"))  # Explicitly redirect to show flash

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/login/google")
def login_google():
    return redirect(url_for("login"))

# ------------------ Dashboard ------------------



# ------------------ DB INIT ------------------
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect, session
from flask_migrate import Migrate
from config import Config
from models import db
from routes.admin import admin_bp
from routes.player import player_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(admin_bp)
app.register_blueprint(player_bp)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        if role == "admin" and request.form["password"] == "testesenha123":
            session["role"] = "admin"
            return redirect("/admin")
        elif role == "player":
            session["role"] = "player"
            return redirect("/player")
    return render_template("login.html")

@app.route("/")
def index():
    role = session.get("role")
    if role == "admin":
        return redirect("/admin")
    elif role == "player":
        return redirect("/player")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()  # remove todas as informações da sessão
    return redirect("/login")  # volta para a tela de login


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

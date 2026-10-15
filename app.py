# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "instagram-clone-secret-2026"

USERS = {
    "admin": "1234",
    "ahmed": "password",
    "user": "0000",
}

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            error = "اسم المستخدم أو كلمة المرور غير صحيحة"
    return render_template("login.html", error=error)

@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html", username=session["username"])

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    print("=" * 50)
    print("  Instagram Login")
    print("  افتح: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
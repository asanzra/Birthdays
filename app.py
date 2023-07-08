import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # DONE: Add the user's entry into the database
        print("POST METHOD")
        name = request.form.get("name")
        try:
            month = int(request.form.get("month"))
            day = int(request.form.get("day"))
        except ValueError:
            # Handle the exception
            print('Numbers not converted correctly')
            return redirect("/")
        if not name or not month or not day:
            print("NAME OR BDAY EMPTY")
            return redirect("/")
        count = db.execute("SELECT COUNT (*) FROM(SELECT * FROM birthdays WHERE name = ?);", name)[0]['COUNT (*)']
        if count > 0:
            print("NAME REPEATED")
            return redirect("/")
        if month > 12 or month < 1 or day < 1 or day > 31:
            print("BDAY DOESNT MAKES SENSE")
            return redirect("/")
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);", name, month, day)
        return redirect("/")

    else:

        # DONE: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays;")
        return render_template("index.html", birthdays = birthdays)



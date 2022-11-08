from flask import Flask, render_template, json
import os

import mysql.connector

app = Flask(__name__)

people_from_app_py = [
    {
        "name": "Thomas",
        "age": 33,
        "location": "New Mexico",
        "favorite_color": "Blue"
    },
    {
        "name": "Gregory",
        "age": 41,
        "location": "Texas",
        "favorite_color": "Red"
    },
    {
        "name": "Vincent",
        "age": 27,
        "location": "Ohio",
        "favorite_color": "Green"
    },
    {
        "name": "Alexander",
        "age": 29,
        "location": "Florida",
        "favorite_color": "Orange"
    }
]

my_db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="bsg"
)


# Routes
@app.route('/')
def root():
    return render_template("main.j2", people=people_from_app_py)


@app.route('/bsg-people')
def bsg_people():
    query = "SELECT * FROM bsg_people;"
    cursor = my_db.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template("bsg.j2", bsg_people=results)


# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 14285))
    # app.run(port=port)
    app.run(port=14285, debug=True)

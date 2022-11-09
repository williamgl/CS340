from flask import Flask, render_template, json, request
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
    password="rootadmin",
    database="ecommerce"
)


# Routes
@app.route('/')
def root():
    return render_template("index.html")


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/customers',methods = ['POST', 'GET'])
def customers():
    if (request.method == 'GET'):
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Customers INNER JOIN CustomerContactInfo ON Customers.customer_id=CustomerContactInfo.customer_id")
        myresult = mycursor.fetchall()
        return render_template("customers.html", myresult=myresult)
    elif request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Customers INNER JOIN CustomerContactInfo ON Customers.customer_id=CustomerContactInfo.customer_id")
        myresult = mycursor.fetchall()
        return render_template("customers.html", myresult=myresult)
        


@app.route('/inventory',methods = ['POST', 'GET'])
def inventory():
    if (request.method == 'GET'):
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Items")
        myresult = mycursor.fetchall()
        return render_template("inventory.html", myresult=myresult)
    elif request.method == 'POST':
        sku = request.form.get("sku")
        country_code = request.form.get("country_code")
        cost = request.form.get("cost")
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Items")
        myresult = mycursor.fetchall()
        return render_template("inventory.html", myresult=myresult)


@app.route('/orders',methods = ['POST', 'GET'])
def orders():
    if (request.method == 'GET'):
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Orders")
        myresult = mycursor.fetchall()
        return render_template("orders.html", myresult=myresult)
    


# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 14285))
    # app.run(port=port)
    app.run(port=8808, debug=True)

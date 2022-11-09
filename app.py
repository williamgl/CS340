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
        if email == None:
            email = ""
        phone = request.form.get("phone")
        if phone == None:
            phone = ""
        mycursor = my_db.cursor()
        
        sql1 = "INSERT INTO Customers (first_name, last_name) VALUES (%s, %s)"
        val1= (first_name,last_name)
        mycursor.execute(sql1, val1)
        my_db.commit()
        
        mycursor.execute("SELECT customer_id FROM Customers WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        myresult = mycursor.fetchall()
        customer_id = myresult[0][0]
        
        sql2 = "INSERT INTO CustomerContactInfo (customer_id, email, phone) VALUES (%s, %s, %s)"
        val2= (customer_id, email,phone)
        mycursor.execute(sql2, val2)
        my_db.commit()
        
        mycursor.execute("SELECT * FROM Customers INNER JOIN CustomerContactInfo ON Customers.customer_id=CustomerContactInfo.customer_id")
        myresult = mycursor.fetchall()
        return render_template("customers.html", myresult=myresult)
        


@app.route('/inventory',methods = ['POST', 'GET'])
def inventory():
    if (request.method == 'GET'):
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Items")
        myresult = mycursor.fetchall()
        mycursor.execute("SELECT * FROM Countries")
        countries = mycursor.fetchall()
        return render_template("inventory.html", myresult=myresult, countries=countries)
    elif request.method == 'POST':
        sku = request.form.get("sku")
        country_code = request.form.get("country_code")
        cost = request.form.get("cost")
        mycursor = my_db.cursor()
        
        sql2 = "INSERT INTO Items (sku, country_code_of_origin, cost) VALUES (%s, %s, %s)"
        val2= (sku,country_code,cost)
        mycursor.execute(sql2, val2)
        my_db.commit()
        
        mycursor.execute("SELECT * FROM Items")
        myresult = mycursor.fetchall()
        mycursor.execute("SELECT * FROM Countries")
        countries = mycursor.fetchall()
        return render_template("inventory.html", myresult=myresult, countries=countries)


@app.route('/orders',methods = ['POST', 'GET'])
def orders():
    if (request.method == 'GET'):
        mycursor = my_db.cursor()
        mycursor.execute("SELECT * FROM Orders")
        myresult = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Customers")
        customers = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Items")
        items = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Countries")
        countries = mycursor.fetchall()
        return render_template("orders.html", myresult=myresult,customers=customers,items=items, countries=countries)
    elif request.method == 'POST':
        mycursor = my_db.cursor()
        customer_id = request.form.get("customer_id")
        item_id = request.form.get("item_id")
        quantity = request.form.get("quantity")
        country_code = request.form.get("country_code")
        item_id = int(item_id)
        
        mycursor.execute("SELECT cost FROM Items WHERE item_id = %s", (item_id,))
        item = mycursor.fetchall()
        item_cost = item[0][0]
        print(item_cost)
        
        total_cost = int(item_cost) * int(quantity)
        
        sql2 = "INSERT INTO Orders (customer_id, total_cost, country_code_of_order) VALUES (%s, %s, %s)"
        val2= (customer_id, total_cost,country_code)
        mycursor.execute(sql2, val2)
        my_db.commit()
        
        mycursor.execute("SELECT * FROM Orders")
        myresult = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Customers")
        customers = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Items")
        items = mycursor.fetchall()
        
        mycursor.execute("SELECT * FROM Countries")
        countries = mycursor.fetchall()
        return render_template("orders.html", myresult=myresult,customers=customers,items=items, countries=countries)
    


# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 14285))
    # app.run(port=port)
    app.run(port=8808, debug=True)

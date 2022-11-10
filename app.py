from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_ligan'
app.config['MYSQL_PASSWORD'] = '5498'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_ligan'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    return redirect("/index")


@app.route('/index')
def index():
    return render_template("index.j2")


@app.route('/customers', methods=['POST', 'GET'])
def customers():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Customers.customer_id AS 'Customer ID',"
                       " first_name AS 'First Name',"
                       " last_name AS 'Last Name',"
                       " email AS Email, phone AS Phone "
                       "FROM Customers INNER JOIN Customer_Info ON Customers.customer_id=Customer_Info.customer_id;")
        result = cursor.fetchall()
        cursor.close()
        return render_template("customers.j2", customers=result)
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]

            cur = mysql.connection.cursor()

            query1 = "INSERT INTO Customers (first_name, last_name) VALUES ('%s', '%s');"
            cur.execute(query1 % (first_name, last_name))
            mysql.connection.commit()

            query2 = "SELECT customer_id FROM Customers WHERE first_name='%s' and last_name='%s';"
            cur.execute(query2 % (first_name, last_name))
            customer_id = cur.fetchone()['customer_id']

            query3 = "INSERT INTO Customer_Info (customer_id, email, phone) VALUES (%d, '%s', '%s');"
            cur.execute(query3 % (customer_id, email, phone))
            mysql.connection.commit()
            cur.close()

            # redirect back to customers page
            return redirect("/customers")


@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customer_id=%d;"
    cur = mysql.connection.cursor()
    cur.execute(query % (customer_id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/customers")


@app.route("/edit_customer/<int:customer_id>", methods=["POST", "GET"])
def edit_customer(customer_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Customers.customer_id, first_name, last_name, email, phone FROM Customers INNER JOIN Customer_Info ON Customers.customer_id=Customer_Info.customer_id WHERE Customers.customer_id=%d;" % (customer_id, )
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_customer.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            # customer_id = request.form["customer_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]

            cur = mysql.connection.cursor()

            query1 = "Update Customers SET first_name='%s', last_name='%s' WHERE customer_id=%d;"
            cur.execute(query1 % (first_name, last_name, customer_id))
            mysql.connection.commit()
            query2 = "Update Customer_Info SET email='%s', phone='%s' WHERE customer_id=%d;"
            cur.execute(query2 % (email, phone, customer_id))
            mysql.connection.commit()
            cur.close()

            # redirect back to customers page
            return redirect("/customers")


@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Items.item_id, sku, cost, location_name, quantity "
                       "FROM Items INNER JOIN Items_Locations ON Items.item_id=Items_Locations.item_id "
                       "INNER JOIN Locations ON Locations.location_id=Items_Locations.location_id;")
        result = cursor.fetchall()
        cursor.close()
        return render_template("inventory.j2", items=result)
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Item"):
            # grab user form inputs
            sku = request.form["sku"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]
            location_id = request.form["location"]

            cur = mysql.connection.cursor()

            # find country_id based on location_id
            query = "SELECT * FROM Locations WHERE location_id=3;"
            cur.exucute(query)
            country_id = cur.fetchall()
            return str(country_id)

            query1 = "INSERT INTO Items (sku, country_id, cost) VALUES ('%s', %d, '%s');"
            cur.execute(query1 % (sku, country_id, cost))
            mysql.connection.commit()

            query2 = "SELECT item_id FROM Items WHERE sku='%s';"
            cur.execute(query2 % (sku, ))
            item_id = cur.fetchone()['item_id']

            query3 = "INSERT INTO Items_Locations (item_id, location_id, quantity) VALUES (%d, %d, %d);"
            cur.execute(query3 % (item_id, location_id, quantity))
            mysql.connection.commit()
            cur.close()

            # redirect back to customers page
            return redirect("/inventory")


"""
@app.route('/orders', methods=['POST', 'GET'])
def orders():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Orders")
        result = cursor.fetchall()
        return render_template("orders.j2", item=result)
"""
@app.route('/countries', methods=['POST', 'GET'])
def countries():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Countries")
        result = cursor.fetchall()
        cursor.close()
        return render_template("countries.html", countries=result)
    

@app.route('/customer_info', methods=['POST', 'GET'])
def customer_info():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Customer_Info")
        result = cursor.fetchall()
        cursor.close()
        return render_template("customer_info.html", customers_info=result)
    
@app.route('/locations', methods=['POST', 'GET'])
def locations():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Locations")
        result = cursor.fetchall()
        cursor.close()
        return render_template("locations.html", locations=result)
    
@app.route('/items', methods=['POST', 'GET'])
def items():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Items")
        result = cursor.fetchall()
        cursor.close()
        return render_template("items.html", items=result)

@app.route('/items_locations', methods=['POST', 'GET'])
def items_locations():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Items_Locations")
        result = cursor.fetchall()
        cursor.close()
        return render_template("items_locations.html", items_locations=result)

@app.route('/items_in_orders', methods=['POST', 'GET'])
def items_in_orders():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Items_In_Orders")
        result = cursor.fetchall()
        cursor.close()
        return render_template("items_in_orders.html", items_in_orders=result)
    
# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 14285))
    # app.run(port=port)
    app.run(port=14285, debug=True)

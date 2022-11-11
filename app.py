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
        cursor.execute("SELECT Customers.customer_id, first_name, last_name, email, phone "
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
    cur.close()
    # redirect back to people page
    return redirect("/customers")


@app.route("/edit_customer/<int:customer_id>", methods=["POST", "GET"])
def edit_customer(customer_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Customers.customer_id, first_name, last_name, email, phone " \
                "FROM Customers INNER JOIN Customer_Info " \
                "ON Customers.customer_id=Customer_Info.customer_id WHERE Customers.customer_id=%d;" % (customer_id, )
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
        cursor.execute("SELECT Items.item_id, sku, cost, quantity, Locations.location_id, location_name "
                       "FROM Items INNER JOIN Items_Locations ON Items.item_id=Items_Locations.item_id "
                       "INNER JOIN Locations ON Locations.location_id=Items_Locations.location_id "
                       "ORDER BY Items.item_id ASC;")
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

            # find country_id based on location_id
            query0 = "SELECT country_id FROM Locations WHERE location_id='%s';"
            cur = mysql.connection.cursor()
            cur.execute(query0 % (location_id,))
            country_id = cur.fetchone()['country_id']

            query1 = "INSERT INTO Items (sku, country_id, cost) VALUES ('%s', %d, '%s');"
            cur.execute(query1 % (sku, country_id, cost))
            mysql.connection.commit()

            query2 = "SELECT item_id FROM Items WHERE sku='%s';"
            cur.execute(query2 % (sku, ))
            item_id = cur.fetchone()['item_id']

            query3 = "INSERT INTO Items_Locations (item_id, location_id, quantity) VALUES (%d, '%s', '%s');"
            cur.execute(query3 % (item_id, location_id, quantity))
            mysql.connection.commit()
            cur.close()

            # redirect back to customers page
            return redirect("/inventory")


@app.route("/delete_item/<int:item_id>/<int:location_id>")
def delete_item(item_id, location_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Items_Locations WHERE item_id=%d and location_id=%d;"
    cur = mysql.connection.cursor()
    cur.execute(query % (item_id, location_id))
    mysql.connection.commit()
    cur.close()
    # redirect back to people page
    return redirect("/inventory")


@app.route("/edit_item/<int:item_id>/<int:location_id>", methods=["POST", "GET"])
def edit_item(item_id, location_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Items.item_id, sku, cost, quantity, Locations.location_id, location_name " \
                "FROM Items INNER JOIN Items_Locations ON Items.item_id=Items_Locations.item_id " \
                "INNER JOIN Locations ON Locations.location_id=Items_Locations.location_id " \
                "WHERE Items.item_id=%d AND Locations.location_id=%d;"
        cur = mysql.connection.cursor()
        cur.execute(query % (item_id, location_id))
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_item.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Item"):
            # grab user form inputs
            # customer_id = request.form["customer_id"]
            sku = request.form["sku"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]
            new_location_id = request.form["location"]

            cur = mysql.connection.cursor()

            query0 = "SELECT country_id FROM Locations WHERE location_id='%s';"
            cur.execute(query0 % (location_id,))
            country_id = cur.fetchone()['country_id']

            cur.execute(query0 % (new_location_id,))
            new_country_id = cur.fetchone()['country_id']

            query2 = "Update Items_Locations SET location_id='%s', quantity='%s' WHERE item_id=%d AND location_id='%s';"
            cur.execute(query2 % (new_location_id, quantity, item_id, location_id))
            query1 = "Update Items SET sku='%s', country_id=%d, cost='%s' WHERE country_id=%d AND item_id=%d;"
            cur.execute(query1 % (sku, new_country_id, cost, country_id, item_id))
            mysql.connection.commit()

            cur.close()

            # redirect back to customers page
            return redirect("/inventory")


@app.route('/orders', methods=['POST', 'GET'])
def orders():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Orders.order_id, customer_id, item_id, quantity "
                       "FROM Orders "
                       "INNER JOIN Items_In_Orders ON Orders.order_id=Items_In_Orders.order_id "
                       "ORDER BY Orders.order_id ASC;")
        result = cursor.fetchall()
        cursor.close()
        return render_template("orders.j2", orders=result)
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Order"):
            # grab user form inputs
            customer_id = request.form["customer_id"]
            item_id = request.form["item_id"]
            quantity = request.form["quantity"]

            cur = mysql.connection.cursor()

            query1 = "INSERT INTO Orders (customer_id) VALUES ('%s');"
            cur.execute(query1 % (customer_id, ))
            mysql.connection.commit()

            query2 = "SELECT order_id FROM Orders WHERE customer_id='%s';"
            cur.execute(query2 % (customer_id, ))
            order_id = cur.fetchall()[-1]['order_id']

            query3 = "INSERT INTO Items_In_Orders (order_id, item_id, quantity) VALUES (%d, '%s', '%s');"
            cur.execute(query3 % (order_id, item_id, quantity))
            mysql.connection.commit()
            cur.close()

            # redirect back to customers page
            return redirect("/orders")


@app.route("/delete_order/<int:order_id>/<int:item_id>")
def delete_order(order_id, item_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Items_In_Orders WHERE order_id=%d and item_id=%d;"
    cur = mysql.connection.cursor()
    cur.execute(query % (order_id, item_id))
    mysql.connection.commit()
    cur.close()
    # redirect back to people page
    return redirect("/orders")


@app.route("/edit_order/<int:item_id>/<int:customer_id>/<int:order_id>", methods=["POST", "GET"])
def edit_order(item_id, customer_id, order_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Orders.order_id, customer_id, item_id, quantity FROM Orders " \
                "INNER JOIN Items_In_Orders ON Orders.order_id=Items_In_Orders.order_id " \
                "WHERE item_id=%d AND customer_id=%d AND Orders.order_id=%d;"
        cur = mysql.connection.cursor()
        cur.execute(query % (item_id, customer_id, order_id))
        data = cur.fetchall()
        cur.close()
        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_order.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Order"):
            # grab user form inputs
            # customer_id = request.form["customer_id"]
            new_order_id = request.form["order_id"]
            new_item_id = request.form["item_id"]
            quantity = request.form["quantity"]

            cur = mysql.connection.cursor()

            query0 = "Update Orders SET order_id='%s' WHERE order_id=%d AND customer_id=%d;"
            cur.execute(query0 % (new_order_id, order_id, customer_id))

            query1 = "Update Items_In_Orders SET order_id='%s', item_id='%s', quantity='%s' " \
                     "WHERE order_id=%d AND item_id=%d;"
            cur.execute(query1 % (new_order_id, new_item_id, quantity, order_id, item_id))
            mysql.connection.commit()

            cur.close()

            # redirect back to customers page
            return redirect("/orders")


# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 14285))
    # app.run(port=port)
    app.run(port=14285, debug=True)

-- These are the queries that our website will use to let the users interact with data. 
-- Thus SELECT, INSERT, UPDATE and DELETE queries to provide the functionalities described in the CS340 Project Guide.

-- SELECT
SELECT * FROM `Countries`;
SELECT * FROM `Customers`;
SELECT * FROM `Customer_Info`;
SELECT * FROM `Items`;
SELECT * FROM `Locations`;
SELECT * FROM `Orders`;
-- select M:M table
SELECT * FROM `Items_In_Orders`;
SELECT * FROM `Items_Locations`;

-- get all first_name and last_name from the Customers table
SELECT first_name, last_name FROM `Customers`;

-- get full customer info from the Customers and Customer_Info tables
SELECT Customers.customer_id, first_name, last_name, email, phone 
FROM `Customers` 
JOIN `Customer_Info` ON Customers.customer_id = Customer_Info.customer_id;

-- INSERT
-- insert customer first name and last name into Customers table
INSERT INTO Customers (first_name, last_name)
VALUES (:first_nameInput, :last_nameInput)

-- insert customer info into Customer_Info table
INSERT INTO Customer_Info (customer_id, email, phone)
VALUES (:customer_idFindByCustomerNameInput, :emailInput, :phoneInput)

-- insert country name and country code into Countries table
INSERT INTO Countries (country, country_code) 
VALUES (:countryInput, :country_codeInput);

-- insert location name into Locations table
INSERT INTO Locations (location_name, country_id)
VALUES (:location_nameInput, :country_idFindByCountryCodeInput);

-- insert item sku, country id, and cost into Items table
INSERT INTO Items (sku, country_id, cost)
VALUES (:skuInput, :country_idFindByCountryCodeInput, :costInput)

--insert customer id and total cost into Orders table
INSERT INTO Orders (customer_id, total_cost)
VALUES (:customer_idFindByCustomerNameInput, :total_costInput)

-- M to M relationship addition
-- insert how many of what item at which location into Items_Locations table
INSERT INTO Items_Locations (item_id, location_id, quantity) 
VALUES (:item_idFindBySkuInput, :location_idInput, :quantityInput)

-- insert item ordered into Items_In_Orders table
INSERT INTO Items_In_Orders (item_id, order_id, quantity)
VALUES (:item_idFindBySkuInput, :order_idInput, :quantityInput)

-- UPDATE
UPDATE Customers 
SET first_name = :first_nameInput, last_name = :last_nameInput 
WHERE customer_id = :customer_idInput;

UPDATE Customer_Info
SET email = :emailInput, phone = :phoneInput
WHERE customer_id = :customer_idInput;

UPDATE Countries
SET country = :countryInput, country_code = :country_codeInput
WHERE country_id = :country_idInput;

UPDATE Locations
SET location_name = :location_nameInput, country_id = :country_idInput
WHERE location_id = :location_idInput;

UPDATE Items
SET sku = :skuInput, country_id = :country_idInput, cost = :costInput
WHERE item_id = :item_idInput;

UPDATE Orders
SET customer_id = :customer_idInput, total_cost = :total_costInput
WHERE order_id = :order_idInput;

-- update the M:M table
UPDATE Items_Locations 
SET item_id = :item_idInput, location_id =:location_idInput, quantity = :quantityInput
WHERE item_to_location_id = :item_to_location_idInput;

UPDATE Items_In_Orders
SET item_id = :item_idInput, order_id =:order_idInput, quantity = :quantityInput
WHERE item_in_orde_id = :item_in_orde_idInput;

-- DELETE
-- DELETE THE TABLE
DROP TABLE `Countries`;
DROP TABLE `Customers`;
DROP TABLE `Customer_Info`;
DROP TABLE `Items`;
DROP TABLE `Locations`;
DROP TABLE `Orders`;
DROP TABLE `Items_In_Orders`;
DROP TABLE `Items_Locations`;

DELETE FROM Countries WHERE country_id = :country_idInput;
DELETE FROM Customers WHERE customer_id = :customer_idInput;
DELETE FROM Customer_Info WHERE customer_id = :customer_idInput;
DELETE FROM Items WHERE item_id = :item_idInput;
DELETE FROM Locations WHERE location_id = :location_idInput;
DELETE FROM Orders WHERE order_id = :order_idInput;
-- delete M:M table
DELETE FROM Items_Locations WHERE item_to_location_id = :item_to_location_idInput;
DELETE FROM Items_In_Orders WHERE item_in_orde_id = :item_in_orde_idInput;
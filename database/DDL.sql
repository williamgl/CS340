-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Table `cs340_ligan`.`Customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Countries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Countries` (
  `country_id` INT NOT NULL AUTO_INCREMENT,
  `country` VARCHAR(255) NOT NULL,
  `country_code` VARCHAR(4) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE INDEX `country_id_UNIQUE` (`country_id` ASC) VISIBLE,
  UNIQUE INDEX `country_code_UNIQUE` (`country_code` ASC) VISIBLE,
  UNIQUE INDEX `country_UNIQUE` (`country` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Items` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `sku` VARCHAR(64) NOT NULL,
  `country_id` INT NOT NULL,
  `cost` FLOAT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`item_id`),
  UNIQUE INDEX `inventory_item_id_UNIQUE` (`item_id` ASC) VISIBLE,
  INDEX `fk_Items_Countries1_idx` (`country_id` ASC) VISIBLE,
  CONSTRAINT `fk_Items_Countries1`
    FOREIGN KEY (`country_id`)
    REFERENCES `cs340_ligan`.`Countries` (`country_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Locations` (
  `location_id` INT NOT NULL AUTO_INCREMENT,
  `location_name` VARCHAR(255) NOT NULL,
  `country_id` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`location_id`),
  UNIQUE INDEX `location_id_UNIQUE` (`location_id` ASC) VISIBLE,
  INDEX `fk_Locations_Countries1_idx` (`country_id` ASC) VISIBLE,
  CONSTRAINT `fk_Locations_Countries1`
    FOREIGN KEY (`country_id`)
    REFERENCES `cs340_ligan`.`Countries` (`country_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `total_cost` FLOAT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE INDEX `order_id_UNIQUE` (`order_id` ASC) VISIBLE,
  INDEX `fk_Orders_Customers_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_Orders_Customers`
    FOREIGN KEY (`customer_id`)
    REFERENCES `cs340_ligan`.`Customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Items_Locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Items_Locations` (
  `item_to_location_id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL,
  `location_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`item_to_location_id`),
  INDEX `fk_InventoryItems_has_InventoryLocations_InventoryLocations_idx` (`location_id` ASC) VISIBLE,
  INDEX `fk_InventoryItems_has_InventoryLocations_InventoryItems1_idx` (`item_id` ASC) VISIBLE,
  UNIQUE INDEX `item_to_location_id_UNIQUE` (`item_to_location_id` ASC) VISIBLE,
  CONSTRAINT `fk_InventoryItems_has_InventoryLocations_InventoryItems1`
    FOREIGN KEY (`item_id`)
    REFERENCES `cs340_ligan`.`Items` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_InventoryItems_has_InventoryLocations_InventoryLocations1`
    FOREIGN KEY (`location_id`)
    REFERENCES `cs340_ligan`.`Locations` (`location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Items_In_Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Items_In_Orders` (
  `item_in_order_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  INDEX `fk_Orders_has_InventoryItems_InventoryItems1_idx` (`item_id` ASC) VISIBLE,
  INDEX `fk_Orders_has_InventoryItems_Orders1_idx` (`order_id` ASC) VISIBLE,
  PRIMARY KEY (`item_in_order_id`),
  UNIQUE INDEX `order_to_item_id_UNIQUE` (`item_in_order_id` ASC) VISIBLE,
  CONSTRAINT `fk_Orders_has_InventoryItems_Orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `cs340_ligan`.`Orders` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Orders_has_InventoryItems_InventoryItems1`
    FOREIGN KEY (`item_id`)
    REFERENCES `cs340_ligan`.`Items` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_ligan`.`Customer_Info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cs340_ligan`.`Customer_Info` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(15) NULL,
  `created_at` TIMESTAMP NOT NULL,
  INDEX `fk_CustomerContactInfo_Customers1_idx` (`customer_id` ASC) VISIBLE,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `Customers_customer_id_UNIQUE` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_CustomerContactInfo_Customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `cs340_ligan`.`Customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO
    Customers (first_name, last_name)
VALUES ("Joe", "Saku"), ("Mary", "Chu"), ("Ivan", "Larrence"), ("Jack", "Smith"), ("Mandy", "Chan"), ("Eric", "Trump");

-- INSERT CUSTOMER NAME

INSERT INTO
    Customer_Info (customer_id, email, phone)
VALUES ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Joe"
                AND last_name = "Saku"
        ),
        "saku@gmail.com",
        "567-123-1234"
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Mary"
                AND last_name = "Chu"
        ),
        "chu@gmail.com",
        "567-123-1235"
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Ivan"
                AND last_name = "Larrence"
        ),
        "larrence@gmail.com",
        "567-123-1236"
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Jack"
                AND last_name = "Smith"
        ),
        "smith@gmail.com",
        "567-123-1237"
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Mandy"
                AND last_name = "Chan"
        ),
        "chan@gmail.com",
        "567-123-1238"
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Eric"
                AND last_name = "Trump"
        ),
        "trump@gmail.com",
        "567-123-1239"
    );

-- INSERT CUSTOMER INFO

INSERT INTO
    Countries (country, country_code) VALUES ("USA", "USA"), ("CANADA", "CAN"), ("JAPAN", "JPN");

INSERT INTO
    Locations (location_name, country_id)
VALUES (
        "1315 Gordon Street, Rancho Cucamonga", (
            SELECT country_id
            FROM Countries
            WHERE
                country_code = "USA"
        )
    ), (
        "3071 Hickory Street, Edmonton", (
            SELECT country_id
            FROM Countries
            WHERE
                country_code = "CAN"
        )
    ), (
        "2683 Red Maple Drive, Irvine", (
            SELECT country_id
            FROM Countries
            WHERE
                country_code = "USA"
        )
    );

INSERT INTO
    Items (
        sku,
        country_id,
        cost
    ) VALUE ("Sho/US-", (
            SELECT country_id 
            FROM Countries 
            WHERE country_code="USA"), 
            33.99), 
        ("Clo/Lar", (
            SELECT country_id 
            FROM Countries 
            WHERE country_code="USA"), 
            50.99), 
        ("PC/Int", (
            SELECT country_id 
            FROM Countries 
            WHERE country_code="USA"),  
            1250.99);

INSERT INTO
    Orders (
        customer_id,
        total_cost
    )
VALUES ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Joe"
                AND last_name = "Saku"
        ),
        250.34
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Mary"
                AND last_name = "Chu"
        ),
        2250.34
    ), ( (
            SELECT
                customer_id
            FROM Customers
            WHERE
                first_name = "Ivan"
                AND last_name = "Larrence"
        ),
        2590.34
    );

INSERT INTO
    Items_Locations (
        item_id, 
        location_id, 
        quantity
        ) VALUES ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Sho/US-"
        ), 1,
        50
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Clo/Lar"
        ), 1,
        60
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "PC/Int"
        ), 1,
        60
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Sho/US-"
        ), 2,
        50
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Clo/Lar"
        ), 2,
        60
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "PC/Int"
        ), 2,
        60
    );

INSERT INTO
    Items_In_Orders (
        item_id,
        order_id,
        quantity
    ) VALUE ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Sho/US-"
        ),
        1,
        1
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Clo/Lar"
        ),
        1,
        1
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "PC/Int"
        ),
        2,
        1
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Sho/US-"
        ),
        2,
        1
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "Clo/Lar"
        ),
        2,
        1
    ), ( (
            SELECT item_id
            FROM Items
            WHERE
                sku = "PC/Int"
        ),
        1,
        1
    );
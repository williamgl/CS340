CREATE TABLE
    IF NOT EXISTS `Customers` (
        `customer_id` INT NOT NULL AUTO_INCREMENT,
        `first_name` VARCHAR(145) NOT NULL,
        `last_name` VARCHAR(145) NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`customer_id`)
    );

CREATE TABLE
    IF NOT EXISTS `CustomerContactInfo` (
        `customer_id` INT NOT NULL AUTO_INCREMENT,
        `email` VARCHAR(145) NOT NULL,
        `phone` VARCHAR(45) NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`customer_id`) REFERENCES `Customers`(`customer_id`) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS `Items` (
        `item_id` INT NOT NULL AUTO_INCREMENT,
        `sku` VARCHAR(145) NOT NULL,
        `country_code_of_origin` VARCHAR(45) NOT NULL,
        `cost` FLOAT NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`item_id`)
    );

CREATE TABLE
    IF NOT EXISTS `Countries` (
        `country_id` INT NOT NULL AUTO_INCREMENT,
        `country_name` VARCHAR(145) NOT NULL,
        `country_code` VARCHAR(45) NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`country_id`)
    );

CREATE TABLE
    IF NOT EXISTS `Locations` (
        `location_id` INT NOT NULL AUTO_INCREMENT,
        `address` VARCHAR(145) NOT NULL,
        `city` VARCHAR(145) NOT NULL,
        `country_id` INT NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`location_id`),
        FOREIGN KEY (`country_id`) REFERENCES `Countries`(`country_id`) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS `Orders` (
        `order_id` INT NOT NULL AUTO_INCREMENT,
        `customer_id` INT NOT NULL,
        `total_cost` FLOAT NOT NULL,
        `country_code_of_order` VARCHAR(45) NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`order_id`),
        FOREIGN KEY (`customer_id`) REFERENCES `Customers`(`customer_id`) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS `ItemsToLocations` (
        `item_to_location_id` INT NOT NULL AUTO_INCREMENT,
        `item_id` INT NOT NULL,
        `location_id` INT NOT NULL,
        `quantity` INT NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`item_to_location_id`),
        FOREIGN KEY (`item_id`) REFERENCES `Items`(`item_id`) ON DELETE CASCADE,
        FOREIGN KEY (`location_id`) REFERENCES `Locations`(`location_id`) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS `OrdersToItems` (
        `order_to_item_id` INT NOT NULL AUTO_INCREMENT,
        `item_id` INT NOT NULL,
        `order_id` INT NOT NULL,
        `quantity_of_item` INT NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`order_to_item_id`),
        FOREIGN KEY (`item_id`) REFERENCES `Items`(`item_id`),
        FOREIGN KEY (`order_id`) REFERENCES `Orders`(`order_id`)
    );
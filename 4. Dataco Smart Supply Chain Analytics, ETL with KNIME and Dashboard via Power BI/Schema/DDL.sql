CREATE DATABASE IF NOT EXISTS `dataco_smart_supply_chain` CHARACTER SET utf8mb4;
USE `dataco_smart_supply_chain`;

CREATE TABLE IF NOT EXISTS `dim_customer` (
  `Id` integer PRIMARY KEY,
  `Name` varchar(255),
  `Segment` varchar(255),
  `Country` varchar(255),
  `City` varchar(255),
  `State` varchar(255),
  `Zipcode` varchar(255),
  `Street` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_shipping` (
  `Id` integer PRIMARY KEY,
  `Mode` varchar(255),
  `Actual_Shipping_Days` integer,
  `Scheduled_Shipping_Days` integer,
  `Late_Delivery_Risk` boolean,
  `Delivery_Status` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_date` (
  `Date` date PRIMARY KEY,
  `Quarter` integer,
  `Year` integer,
  `Month` integer,
  `Day` integer
);

CREATE TABLE IF NOT EXISTS `dim_product` (
  `Id` integer PRIMARY KEY,
  `Name` varchar(255),
  `Price` float,
  `Image` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_department` (
  `Id` integer PRIMARY KEY,
  `Department` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_product_category` (
  `Id` integer PRIMARY KEY,
  `Category` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_order_territory` (
  `Id` integer PRIMARY KEY,
  `Region` varchar(255),
  `Country` varchar(255),
  `State` varchar(255),
  `City` varchar(255)
);

CREATE TABLE IF NOT EXISTS `dim_store_location` (
  `Id` integer PRIMARY KEY,
  `Latitude` float,
  `Longitude` float
);

CREATE TABLE IF NOT EXISTS `fact_order` (
  `Id` integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Order_Id` integer NOT NULL,
  `Customer_Id` integer,
  `Shipping_Id` integer,
  `Product_Id` integer,
  `Department_Id` integer,
  `Product_Category_Id` integer,
  `Order_Territory_Id` integer,
  `Store_Location_Id` integer,
  `Order_Date` date,
  `Shipping_Date` date,
  `Market` varchar(255),
  `Item_Id` integer,
  `Item_Quantity` integer,
  `Item_Price` float,
  `Item_Discount` float,
  `Item_Total` float,
  `Sales` float,
  `Order_Profit_Per_Order` float,
  `Payment_Method` varchar(255),
  `Order_Status` varchar(255),
  INDEX `idx_fact_order_order_id` (`Order_Id`),
  FOREIGN KEY (`Customer_Id`) REFERENCES `dim_customer` (`Id`),
  FOREIGN KEY (`Shipping_Id`) REFERENCES `dim_shipping` (`Id`),
  FOREIGN KEY (`Product_Id`) REFERENCES `dim_product` (`Id`),
  FOREIGN KEY (`Department_Id`) REFERENCES `dim_department` (`Id`),
  FOREIGN KEY (`Product_Category_Id`) REFERENCES `dim_product_category` (`Id`),
  FOREIGN KEY (`Order_Territory_Id`) REFERENCES `dim_order_territory` (`Id`),
  FOREIGN KEY (`Store_Location_Id`) REFERENCES `dim_store_location` (`Id`),
  FOREIGN KEY (`Order_Date`) REFERENCES `dim_date` (`Date`),
  FOREIGN KEY (`Shipping_Date`) REFERENCES `dim_date` (`Date`)
);
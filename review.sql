-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`customer` (
  `customer_id's` INT NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `address` VARCHAR(100) NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`customer_id's`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`category_id`));


-- -----------------------------------------------------
-- Table `mydb`.`author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`author` (
  `author_id` INT NOT NULL,
  `author's_name` VARCHAR(45) NOT NULL,
  `author's_lastname` VARCHAR(45) NULL,
  PRIMARY KEY (`author_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Shopping_cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Shopping_cart` (
  `idShopping_cart` INT NOT NULL,
  `customer_id's` INT NOT NULL,
  PRIMARY KEY (`idShopping_cart`),
  INDEX `customer_id's_idx` (`customer_id's` ASC) VISIBLE,
  CONSTRAINT `customer_id's`
    FOREIGN KEY (`customer_id's`)
    REFERENCES `mydb`.`customer` (`customer_id's`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`order` (
  `order_id's` INT NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `customer_idcustomer` INT NOT NULL,
  `total_amount` DECIMAL(10,2) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `Shopping_cart_idShopping_cart` INT NOT NULL,
  INDEX `fk_order_customer_idx` (`customer_idcustomer` ASC) VISIBLE,
  PRIMARY KEY (`order_id's`),
  INDEX `fk_order_Shopping_cart1_idx` (`Shopping_cart_idShopping_cart` ASC) VISIBLE,
  CONSTRAINT `fk_order_customer`
    FOREIGN KEY (`customer_idcustomer`)
    REFERENCES `mydb`.`customer` (`customer_id's`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_Shopping_cart1`
    FOREIGN KEY (`Shopping_cart_idShopping_cart`)
    REFERENCES `mydb`.`Shopping_cart` (`idShopping_cart`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Order_Items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Order_Items` (
  `idOrder_Items` INT NOT NULL,
  `order_id` INT NOT NULL,
  `book_id's` INT NULL,
  `price` INT NULL,
  `order_order_id's` INT NOT NULL,
  PRIMARY KEY (`idOrder_Items`),
  INDEX `fk_Order_Items_order1_idx` (`order_order_id's` ASC) VISIBLE,
  CONSTRAINT `fk_Order_Items_order1`
    FOREIGN KEY (`order_order_id's`)
    REFERENCES `mydb`.`order` (`order_id's`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`book` (
  `book_id's` INT NOT NULL,
  `book's_name` VARCHAR(100) NOT NULL,
  `author_id` INT NOT NULL,
  `category_category_id` INT NOT NULL,
  `price` DECIMAL(10,2) NULL,
  `quantity` INT NOT NULL,
  `author_author_id` INT NOT NULL,
  `Order_Items_idOrder_Items` INT NOT NULL,
  PRIMARY KEY (`book_id's`),
  INDEX `fk_book_category1_idx` (`category_category_id` ASC) VISIBLE,
  INDEX `fk_book_author1_idx` (`author_author_id` ASC) VISIBLE,
  INDEX `fk_book_Order_Items1_idx` (`Order_Items_idOrder_Items` ASC) VISIBLE,
  CONSTRAINT `fk_book_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `mydb`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_book_author1`
    FOREIGN KEY (`author_author_id`)
    REFERENCES `mydb`.`author` (`author_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_book_Order_Items1`
    FOREIGN KEY (`Order_Items_idOrder_Items`)
    REFERENCES `mydb`.`Order_Items` (`idOrder_Items`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`category_has_author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`category_has_author` (
  `category_category_id` INT NOT NULL,
  `author_author_id` INT NOT NULL,
  INDEX `fk_category_has_author_category1_idx` (`category_category_id` ASC) VISIBLE,
  INDEX `fk_category_has_author_author1_idx` (`author_author_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_has_author_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `mydb`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_has_author_author1`
    FOREIGN KEY (`author_author_id`)
    REFERENCES `mydb`.`author` (`author_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`Shopping_cart_has_book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Shopping_cart_has_book` (
  `Shopping_cart_idShopping_cart` INT NOT NULL,
  `book_book_id's` INT NOT NULL,
  PRIMARY KEY (`Shopping_cart_idShopping_cart`, `book_book_id's`),
  INDEX `fk_Shopping_cart_has_book_book1_idx` (`book_book_id's` ASC) VISIBLE,
  INDEX `fk_Shopping_cart_has_book_Shopping_cart1_idx` (`Shopping_cart_idShopping_cart` ASC) VISIBLE,
  CONSTRAINT `fk_Shopping_cart_has_book_Shopping_cart1`
    FOREIGN KEY (`Shopping_cart_idShopping_cart`)
    REFERENCES `mydb`.`Shopping_cart` (`idShopping_cart`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Shopping_cart_has_book_book1`
    FOREIGN KEY (`book_book_id's`)
    REFERENCES `mydb`.`book` (`book_id's`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Order_Items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Order_Items` (
  `idOrder_Items` INT NOT NULL,
  `order_id` INT NOT NULL,
  `book_id's` INT NULL,
  `price` INT NULL,
  `order_order_id's` INT NOT NULL,
  PRIMARY KEY (`idOrder_Items`),
  INDEX `fk_Order_Items_order1_idx` (`order_order_id's` ASC) VISIBLE,
  CONSTRAINT `fk_Order_Items_order1`
    FOREIGN KEY (`order_order_id's`)
    REFERENCES `mydb`.`order` (`order_id's`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

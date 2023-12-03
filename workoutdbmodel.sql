-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema workoutdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema workoutdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `workoutdb` DEFAULT CHARACTER SET utf8 ;
USE `workoutdb` ;

-- -----------------------------------------------------
-- Table `workoutdb`.`type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`type` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(45) NULL,
  `desc` VARCHAR(255) NULL,
  PRIMARY KEY (`type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`level`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`level` (
  `level_id` INT NOT NULL AUTO_INCREMENT,
  `level_name` VARCHAR(45) NULL,
  `desc` VARCHAR(255) NULL,
  PRIMARY KEY (`level_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`account` (
  `account_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `role` VARCHAR(45) NULL,
  `date_registered` DATETIME NULL,
  PRIMARY KEY (`account_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`instructor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`instructor` (
  `instructor_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT 'Jenny',
  `email` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `account_id` INT NULL,
  `dob` DATE NULL,
  `ssn` VARCHAR(45) NULL,
  PRIMARY KEY (`instructor_id`),
  INDEX `FK_instructor_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `FK_instructor_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `workoutdb`.`account` (`account_id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`schedule`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`schedule` (
  `schedule_id` INT NOT NULL AUTO_INCREMENT,
  `duration` SMALLINT(2) NULL,
  `start_time` DATETIME NULL,
  `end_time` DATETIME NULL,
  PRIMARY KEY (`schedule_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`workout_class`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`workout_class` (
  `class_id` INT NOT NULL AUTO_INCREMENT COMMENT '1\n',
  `level` INT NULL,
  `class_title` VARCHAR(45) NOT NULL,
  `location` VARCHAR(100) NULL,
  `type` INT NULL,
  `instructor_id` INT NULL,
  `schedule_id` INT NOT NULL,
  `description` VARCHAR(255) NULL,
  PRIMARY KEY (`class_id`),
  INDEX `FK_class_type_id_idx` (`type` ASC) VISIBLE,
  INDEX `FK_class_level_id_idx` (`level` ASC) VISIBLE,
  INDEX `FK_class_instructor_id_idx` (`instructor_id` ASC) VISIBLE,
  INDEX `FK_class_schedule_id_idx` (`schedule_id` ASC) VISIBLE,
  CONSTRAINT `FK_class_type_id`
    FOREIGN KEY (`type`)
    REFERENCES `workoutdb`.`type` (`type_id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_class_level_id`
    FOREIGN KEY (`level`)
    REFERENCES `workoutdb`.`level` (`level_id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
  CONSTRAINT `FK_class_instructor_id`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `workoutdb`.`instructor` (`instructor_id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_class_schedule_id`
    FOREIGN KEY (`schedule_id`)
    REFERENCES `workoutdb`.`schedule` (`schedule_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`member` (
  `tracking_id` INT NOT NULL AUTO_INCREMENT,
  `class_id` INT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`tracking_id`),
  INDEX `FK_member_class_id_idx` (`class_id` ASC) VISIBLE,
  CONSTRAINT `FK_member_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `workoutdb`.`workout_class` (`class_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`membership`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`membership` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `membership_tye` VARCHAR(45) NULL,
  `pricing` INT NULL,
  `start_date` DATETIME NULL,
  `end_date` DATETIME NULL,
  `auto_pay` TINYINT NULL DEFAULT 1 COMMENT 'True - 1\nFalse- 0\n\n',
  `account_id` INT NULL,
  PRIMARY KEY (`member_id`),
  INDEX `FK_membership_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `FK_membership_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `workoutdb`.`account` (`account_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`booking_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`booking_history` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `class_id` INT NULL,
  `booking_date` DATETIME NULL,
  `cancellation_date` DATETIME NULL,
  `status` VARCHAR(45) NULL,
  PRIMARY KEY (`booking_id`),
  INDEX `FK_history_member_id_idx` (`member_id` ASC) VISIBLE,
  INDEX `FK_hisotry_class_id_idx` (`class_id` ASC) VISIBLE,
  CONSTRAINT `FK_history_member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `workoutdb`.`membership` (`member_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_hisotry_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `workoutdb`.`workout_class` (`class_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`certification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`certification` (
  `certification_id` INT NOT NULL AUTO_INCREMENT,
  `instructor_id` INT NULL,
  `name` VARCHAR(45) NULL,
  `issuing_organization` VARCHAR(50) NULL,
  `expiration_date` DATETIME NULL,
  PRIMARY KEY (`certification_id`),
  INDEX `FK_certification_instructor_id_idx` (`instructor_id` ASC) VISIBLE,
  CONSTRAINT `FK_certification_instructor_id`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `workoutdb`.`instructor` (`instructor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`facility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`facility` (
  `facility_id` INT NOT NULL AUTO_INCREMENT,
  `facility_name` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` CHAR(2) NULL,
  `postal_code` VARCHAR(10) NULL,
  `operation_hours` VARCHAR(45) NULL,
  `occupancy` INT NULL,
  PRIMARY KEY (`facility_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`equipment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`equipment` (
  `equipment_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `quantity` SMALLINT(3) NULL,
  `serial_number` VARCHAR(45) NULL,
  `purchase_date` DATETIME NULL,
  `price` INT NULL,
  `condition` VARCHAR(45) NULL,
  `last_maintenance_date` DATETIME NULL,
  `facility_id` INT NULL,
  PRIMARY KEY (`equipment_id`),
  INDEX `FK_equipment_facility_id_idx` (`facility_id` ASC) VISIBLE,
  CONSTRAINT `FK_equipment_facility_id`
    FOREIGN KEY (`facility_id`)
    REFERENCES `workoutdb`.`facility` (`facility_id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`purchase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`purchase` (
  `transation_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `price` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `payment_method` VARCHAR(45) NULL,
  PRIMARY KEY (`transation_id`),
  INDEX `FK_purchase_member_id_idx` (`member_id` ASC) VISIBLE,
  CONSTRAINT `FK_purchase_member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `workoutdb`.`membership` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`admin` (
  `admin_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `title` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `account_id` INT NULL,
  `phone` VARCHAR(45) NULL,
  `dob` DATE NULL,
  `ssn` VARCHAR(45) NULL,
  PRIMARY KEY (`admin_id`),
  INDEX `FK_admin_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `FK_admin_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `workoutdb`.`account` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`manager`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`manager` (
  `manager_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `hire_date` DATE NULL,
  `account_id` INT NULL,
  `dob` DATE NULL,
  `ssn` VARCHAR(45) NULL,
  PRIMARY KEY (`manager_id`),
  INDEX `FK_manager_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `FK_manager_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `workoutdb`.`account` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`review` (
  `review_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `rating` TINYINT(1) NULL,
  `comment` TINYTEXT NULL,
  `review_date` DATETIME NULL,
  `class_id` INT NULL,
  PRIMARY KEY (`review_id`),
  INDEX `FK_review_member_id_idx` (`member_id` ASC) VISIBLE,
  INDEX `FL_review_class_id_idx` (`class_id` ASC) VISIBLE,
  CONSTRAINT `FK_review_member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `workoutdb`.`membership` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FL_review_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `workoutdb`.`workout_class` (`class_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`trainingGoal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`trainingGoal` (
  `goal_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `goal_type` VARCHAR(45) NULL,
  `start_date` DATETIME NULL,
  `target_date` DATETIME NULL,
  `status` VARCHAR(45) NULL,
  PRIMARY KEY (`goal_id`),
  INDEX `FK_goal_member_id_idx` (`member_id` ASC) VISIBLE,
  CONSTRAINT `FK_goal_member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `workoutdb`.`membership` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`metrics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`metrics` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `weight` DECIMAL(5,2) NULL,
  `height` SMALLINT(3) NULL,
  PRIMARY KEY (`record_id`),
  INDEX `FK_ metrics_member_id_idx` (`member_id` ASC) VISIBLE,
  CONSTRAINT `FK_ metrics_member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `workoutdb`.`membership` (`member_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workoutdb`.`employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workoutdb`.`employee` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `hire_date` DATE NULL,
  `account_id` INT NULL,
  `dob` DATE NULL,
  `ssn` VARCHAR(45) NULL,
  PRIMARY KEY (`employee_id`),
  INDEX `FK_employee_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `FK_employee_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `workoutdb`.`account` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

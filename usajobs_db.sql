-- MySQL Script generated by MySQL Workbench
-- Thu Nov 24 15:44:43 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`agencies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`agencies` ;

CREATE TABLE IF NOT EXISTS `mydb`.`agencies` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `department` INT NULL COMMENT 'Refers to the departments table',
  `address` VARCHAR(450) NULL,
  `email` VARCHAR(100) NULL,
  `phone` VARCHAR(45) NULL,
  `website` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`),
  INDEX `department_idx` (`department` ASC) VISIBLE,
  CONSTRAINT `department`
    FOREIGN KEY (`department`)
    REFERENCES `mydb`.`departments` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`appointment_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`appointment_type` ;

CREATE TABLE IF NOT EXISTS `mydb`.`appointment_type` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NULL,
  `permanent` INT NULL COMMENT 'General - if it is permanent or temporary',
  `term` INT NULL COMMENT 'In years, if indicated',
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`category` ;

CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`departments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`departments` ;

CREATE TABLE IF NOT EXISTS `mydb`.`departments` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`job_card`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`job_card` ;

CREATE TABLE IF NOT EXISTS `mydb`.`job_card` (
  `ID` INT NOT NULL AUTO_INCREMENT COMMENT 'Auto - increment ID of the card',
  `name` VARCHAR(100) NOT NULL COMMENT 'Title of the position\n',
  `agency_id` INT NOT NULL COMMENT 'Agency ID refers to the agency in the table agencies\n',
  `professional_area` INT NULL COMMENT 'Refers to the professional field (e.g. Chemistry, Computer science) as listed on the starting page',
  `summary` VARCHAR(4000) NULL COMMENT 'Text of the Summary section \n',
  `duties` VARCHAR(4000) NULL COMMENT 'Text of the duties section\n',
  `requirements_id` INT NULL COMMENT 'Refers to the table with Requirement section contents\n',
  `evaluation` VARCHAR(3000) NULL COMMENT ' text of the Evaluation section\n',
  `req_docs` VARCHAR(3000) NULL COMMENT ' text of the Required documents section',
  `how_to_apply` VARCHAR(3000) NULL COMMENT ' text of the How to apply section',
  `start_date` DATETIME NULL COMMENT 'Date of the opening of the position',
  `end_date` DATETIME NULL COMMENT 'Date of the closing of the position',
  `start_salary` INT NULL COMMENT 'Lower value in the salary range as indicated in overview',
  `max_salary` INT NULL COMMENT 'Higher value in the salary range as indicated in overview',
  `salary_comment` VARCHAR(300) NULL COMMENT 'From Overview / Salary the text besides the numbers',
  `pay_scale_&_grade_id` INT NULL COMMENT 'Pay scale and grade as indicated in the overview\nRefers to the table',
  `job_family_(series)_id` INT NULL COMMENT 'Job family  as indicated in the overview\nRefers to the table',
  `remote` INT NULL,
  `telework_eligible_id` INT NULL COMMENT 'Is telework possible from Overview\nRefers to the table',
  `travel_required_id` INT NULL COMMENT 'Is travel allowed from Overview\nRefers to the table',
  `relocation_expenses_reimbursed_id` INT NULL COMMENT 'Are relocation expenses reimbursed \nRefers to the table',
  `appointment_type_id` INT NULL COMMENT 'Appointment type from Overview\nRefers to the table',
  `work_schedule_id` INT NULL COMMENT 'Work schedule from Overview\nRefers to the table',
  `supervisory_status` INT NULL COMMENT 'Supervisory status\nBinary (yes/no)',
  `security_clearance_id` INT NULL COMMENT 'Security clearance\nTakes three values\nRefers tot he table',
  `drug_test` INT NULL COMMENT 'Is drug test required from Overview\nBinary Yes/No\n',
  `position_sensitivity_and_risk_id` INT NULL COMMENT 'Sensitivity from Overview\nRefers to the table',
  `trust_determination_process_id` INT NULL COMMENT 'Trust determination process from Overview\nTakes 3 values\nRefers to the table',
  `promotion_potential_id` INT NULL COMMENT 'From Overview / Promotion potential\nRefers to the table',
  `service_id` INT NULL COMMENT 'From Overview/service \nTakes 3 values\nRefers to the table ',
  `announcement_number` VARCHAR(20) NULL COMMENT 'Announce no from Overview',
  `control_number` INT NULL COMMENT 'Control number from Overview',
  PRIMARY KEY (`ID`),
  INDEX `scale_grade_idx` (`pay_scale_&_grade_id` ASC) VISIBLE,
  INDEX `telework_idx` (`telework_eligible_id` ASC) VISIBLE,
  INDEX `travel_idx` (`travel_required_id` ASC) VISIBLE,
  INDEX `reloc_idx` (`relocation_expenses_reimbursed_id` ASC) VISIBLE,
  INDEX `appointment_idx` (`appointment_type_id` ASC) VISIBLE,
  INDEX `work_sch_idx` (`work_schedule_id` ASC) VISIBLE,
  INDEX `service_idx` (`service_id` ASC) VISIBLE,
  INDEX `prom_poten_idx` (`promotion_potential_id` ASC) VISIBLE,
  INDEX `job_fam_idx` (`job_family_(series)_id` ASC) VISIBLE,
  INDEX `security_idx` (`security_clearance_id` ASC) VISIBLE,
  INDEX `sens_trust_idx` (`position_sensitivity_and_risk_id` ASC) VISIBLE,
  INDEX `trust_idx` (`trust_determination_process_id` ASC) VISIBLE,
  INDEX `agency_idx` (`agency_id` ASC) VISIBLE,
  INDEX `requirements_idx` (`requirements_id` ASC) VISIBLE,
  INDEX `prof_area_idx` (`professional_area` ASC) VISIBLE,
  CONSTRAINT `scale_grade`
    FOREIGN KEY (`pay_scale_&_grade_id`)
    REFERENCES `mydb`.`pay_scale_&_grade` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `telework`
    FOREIGN KEY (`telework_eligible_id`)
    REFERENCES `mydb`.`telework_eligible` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `travel`
    FOREIGN KEY (`travel_required_id`)
    REFERENCES `mydb`.`travel_required` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `reloc`
    FOREIGN KEY (`relocation_expenses_reimbursed_id`)
    REFERENCES `mydb`.`relocation_expenses_reimbursed` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `appointment`
    FOREIGN KEY (`appointment_type_id`)
    REFERENCES `mydb`.`appointment_type` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `work_sch`
    FOREIGN KEY (`work_schedule_id`)
    REFERENCES `mydb`.`work_schedule` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `service`
    FOREIGN KEY (`service_id`)
    REFERENCES `mydb`.`service` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `prom_poten`
    FOREIGN KEY (`promotion_potential_id`)
    REFERENCES `mydb`.`promotion_potential` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `job_fam`
    FOREIGN KEY (`job_family_(series)_id`)
    REFERENCES `mydb`.`job_family_(series)` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `security`
    FOREIGN KEY (`security_clearance_id`)
    REFERENCES `mydb`.`security_clearance` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `sens_trust`
    FOREIGN KEY (`position_sensitivity_and_risk_id`)
    REFERENCES `mydb`.`position_sensitivity_and_risk` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `trust`
    FOREIGN KEY (`trust_determination_process_id`)
    REFERENCES `mydb`.`trust_determination_process` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `agency`
    FOREIGN KEY (`agency_id`)
    REFERENCES `mydb`.`agencies` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `requirements`
    FOREIGN KEY (`requirements_id`)
    REFERENCES `mydb`.`requirements` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `prof_area`
    FOREIGN KEY (`professional_area`)
    REFERENCES `mydb`.`prof_area` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`job_family_(series)`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`job_family_(series)` ;

CREATE TABLE IF NOT EXISTS `mydb`.`job_family_(series)` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NULL,
  `num_index` INT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`locations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`locations` ;

CREATE TABLE IF NOT EXISTS `mydb`.`locations` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `coord` VARCHAR(45) NULL,
  `comment` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`pay_scale_&_grade`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`pay_scale_&_grade` ;

CREATE TABLE IF NOT EXISTS `mydb`.`pay_scale_&_grade` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`pos_at_loc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`pos_at_loc` ;

CREATE TABLE IF NOT EXISTS `mydb`.`pos_at_loc` (
  `job_card_id` INT NOT NULL,
  `location_id` INT NULL,
  `num_of_vacancies` INT NULL,
  PRIMARY KEY (`job_card_id`),
  INDEX `location_idx` (`location_id` ASC) VISIBLE,
  CONSTRAINT `position`
    FOREIGN KEY (`job_card_id`)
    REFERENCES `mydb`.`job_card` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `location`
    FOREIGN KEY (`location_id`)
    REFERENCES `mydb`.`locations` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`position_sensitivity_and_risk`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`position_sensitivity_and_risk` ;

CREATE TABLE IF NOT EXISTS `mydb`.`position_sensitivity_and_risk` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`prof_area`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`prof_area` ;

CREATE TABLE IF NOT EXISTS `mydb`.`prof_area` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `category` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `category_idx` (`category` ASC) VISIBLE,
  CONSTRAINT `category`
    FOREIGN KEY (`category`)
    REFERENCES `mydb`.`category` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`promotion_potential`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`promotion_potential` ;

CREATE TABLE IF NOT EXISTS `mydb`.`promotion_potential` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NOT NULL,
  `level` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`relocation_expenses_reimbursed`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`relocation_expenses_reimbursed` ;

CREATE TABLE IF NOT EXISTS `mydb`.`relocation_expenses_reimbursed` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NULL,
  `gen_yesno` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`requirements`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`requirements` ;

CREATE TABLE IF NOT EXISTS `mydb`.`requirements` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(5000) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`security_clearance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`security_clearance` ;

CREATE TABLE IF NOT EXISTS `mydb`.`security_clearance` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`service` ;

CREATE TABLE IF NOT EXISTS `mydb`.`service` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`telework_eligible`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`telework_eligible` ;

CREATE TABLE IF NOT EXISTS `mydb`.`telework_eligible` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NOT NULL,
  `eligibility` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`travel_required`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`travel_required` ;

CREATE TABLE IF NOT EXISTS `mydb`.`travel_required` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NULL,
  `general_yes_no` INT NULL,
  `time_percentage` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`trust_determination_process`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`trust_determination_process` ;

CREATE TABLE IF NOT EXISTS `mydb`.`trust_determination_process` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`work_schedule`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`work_schedule` ;

CREATE TABLE IF NOT EXISTS `mydb`.`work_schedule` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NULL,
  `full_time` INT NULL COMMENT 'Is it full-time (yes/no)',
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

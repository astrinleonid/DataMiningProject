-- MySQL Script generated by MySQL Workbench
-- Wed Nov 23 14:37:16 2022
-- Model: New Model    Version: 1.0
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
-- Table `mydb`.`agencies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`agencies` ;

CREATE TABLE IF NOT EXISTS `mydb`.`agencies` (
  `ID` INT NOT NULL,
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
-- Table `mydb`.`app_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`app_type` ;

CREATE TABLE IF NOT EXISTS `mydb`.`app_type` (
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
  `section` INT NULL COMMENT 'Refers to the professional field (e.g. Chemistry, Computer science) as listed on the starting page',
  `summary` VARCHAR(4000) NULL COMMENT 'Text of the Summary section \n',
  `duties` VARCHAR(4000) NULL COMMENT 'Text of the duties section\n',
  `requirements` INT NULL COMMENT 'Refers to the table with Requirement section contents\n',
  `evaluation` VARCHAR(3000) NULL COMMENT ' text of the Evaluation section\n',
  `req_docs` VARCHAR(3000) NULL COMMENT ' text of the Required documents section',
  `how_to_apply` VARCHAR(3000) NULL COMMENT ' text of the How to apply section',
  `start_date` DATETIME NULL COMMENT 'Date of the opening of the position',
  `end_date` DATETIME NULL COMMENT 'Date of the closing of the position',
  `start_salary` INT NULL COMMENT 'Lower value in the salary range as indicated in overview',
  `max_salary` INT NULL COMMENT 'Higher value in the salary range as indicated in overview',
  `salary_comment` VARCHAR(300) NULL COMMENT 'From Overview / Salary the text besides the numbers',
  `pay_scale_grade` INT NULL COMMENT 'Pay scale and grade as indicated in the overview\nRefers to the table',
  `job_family` INT NULL COMMENT 'Job family  as indicated in the overview\nRefers to the table',
  `remote` INT NULL,
  `telework` INT NULL COMMENT 'Is telework possible from Overview\nRefers to the table',
  `travel` INT NULL COMMENT 'Is travel allowed from Overview\nRefers to the table',
  `relocation_exp` INT NULL COMMENT 'Are relocation expenses reimbursed \nRefers to the table',
  `app_type` INT NULL COMMENT 'Appointment type from Overview\nRefers to the table',
  `work_schedule` INT NULL COMMENT 'Work schedule from Overview\nRefers to the table',
  `supervisory` INT NULL COMMENT 'Supervisory status\nBinary (yes/no)',
  `security` INT NULL COMMENT 'Security clearance\nTakes three values\nRefers tot he table',
  `drug` INT NULL COMMENT 'Is drug test required from Overview\nBinary Yes/No\n',
  `sensitivity` INT NULL COMMENT 'Sensitivity from Overview\nRefers to the table',
  `trust` INT NULL COMMENT 'Trust determination process from Overview\nTakes 3 values\nRefers to the table',
  `promotion` INT NULL COMMENT 'From Overview / Promotion potential\nRefers to the table',
  `service` INT NULL COMMENT 'From Overview/service \nTakes 3 values\nRefers to the table ',
  `announce_no` VARCHAR(20) NULL COMMENT 'Announce no from Overview',
  `control_no` INT NULL COMMENT 'Control number from Overview',
  PRIMARY KEY (`ID`),
  INDEX `scale_grade_idx` (`pay_scale_grade` ASC) VISIBLE,
  INDEX `telework_idx` (`telework` ASC) VISIBLE,
  INDEX `travel_idx` (`travel` ASC) VISIBLE,
  INDEX `reloc_idx` (`relocation_exp` ASC) VISIBLE,
  INDEX `appointment_idx` (`app_type` ASC) VISIBLE,
  INDEX `work_sch_idx` (`work_schedule` ASC) VISIBLE,
  INDEX `service_idx` (`service` ASC) VISIBLE,
  INDEX `prom_poten_idx` (`promotion` ASC) VISIBLE,
  INDEX `job_fam_idx` (`job_family` ASC) VISIBLE,
  INDEX `security_idx` (`security` ASC) VISIBLE,
  INDEX `sens_trust_idx` (`sensitivity` ASC) VISIBLE,
  INDEX `trust_idx` (`trust` ASC) VISIBLE,
  INDEX `agency_idx` (`agency_id` ASC) VISIBLE,
  INDEX `requirements_idx` (`requirements` ASC) VISIBLE,
  INDEX `prof_area_idx` (`section` ASC) VISIBLE,
  CONSTRAINT `scale_grade`
    FOREIGN KEY (`pay_scale_grade`)
    REFERENCES `mydb`.`pay_scale&grade` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `telework`
    FOREIGN KEY (`telework`)
    REFERENCES `mydb`.`telework` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `travel`
    FOREIGN KEY (`travel`)
    REFERENCES `mydb`.`travel` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `reloc`
    FOREIGN KEY (`relocation_exp`)
    REFERENCES `mydb`.`reloc_reimburse` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `appointment`
    FOREIGN KEY (`app_type`)
    REFERENCES `mydb`.`app_type` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `work_sch`
    FOREIGN KEY (`work_schedule`)
    REFERENCES `mydb`.`work_scedule` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `service`
    FOREIGN KEY (`service`)
    REFERENCES `mydb`.`service` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `prom_poten`
    FOREIGN KEY (`promotion`)
    REFERENCES `mydb`.`prom_potential` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `job_fam`
    FOREIGN KEY (`job_family`)
    REFERENCES `mydb`.`job_family` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `security`
    FOREIGN KEY (`security`)
    REFERENCES `mydb`.`Sec_clearance` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `sens_trust`
    FOREIGN KEY (`sensitivity`)
    REFERENCES `mydb`.`sens&trust` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `trust`
    FOREIGN KEY (`trust`)
    REFERENCES `mydb`.`trust_procedure` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `agency`
    FOREIGN KEY (`agency_id`)
    REFERENCES `mydb`.`agencies` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `requirements`
    FOREIGN KEY (`requirements`)
    REFERENCES `mydb`.`requirements` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `prof_area`
    FOREIGN KEY (`section`)
    REFERENCES `mydb`.`prof_area` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`job_family`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`job_family` ;

CREATE TABLE IF NOT EXISTS `mydb`.`job_family` (
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
-- Table `mydb`.`pay_scale&grade`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`pay_scale&grade` ;

CREATE TABLE IF NOT EXISTS `mydb`.`pay_scale&grade` (
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
-- Table `mydb`.`prom_potential`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`prom_potential` ;

CREATE TABLE IF NOT EXISTS `mydb`.`prom_potential` (
  `ID` INT NOT NULL,
  `text` VARCHAR(450) NOT NULL,
  `level` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`reloc_reimburse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`reloc_reimburse` ;

CREATE TABLE IF NOT EXISTS `mydb`.`reloc_reimburse` (
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
  `ID` INT NOT NULL,
  `text` VARCHAR(5000) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Sec_clearance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Sec_clearance` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Sec_clearance` (
  `ID` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sens&trust`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`sens&trust` ;

CREATE TABLE IF NOT EXISTS `mydb`.`sens&trust` (
  `ID` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`service` ;

CREATE TABLE IF NOT EXISTS `mydb`.`service` (
  `ID` INT NOT NULL,
  `text` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`telework`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`telework` ;

CREATE TABLE IF NOT EXISTS `mydb`.`telework` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(450) NOT NULL,
  `eligibility` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`travel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`travel` ;

CREATE TABLE IF NOT EXISTS `mydb`.`travel` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NULL,
  `general_yes_no` INT NULL,
  `time_percentage` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`trust_procedure`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`trust_procedure` ;

CREATE TABLE IF NOT EXISTS `mydb`.`trust_procedure` (
  `ID` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`work_scedule`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`work_scedule` ;

CREATE TABLE IF NOT EXISTS `mydb`.`work_scedule` (
  `ID` INT NOT NULL,
  `text` VARCHAR(450) NULL,
  `full_time` INT NULL COMMENT 'Is it full-time (yes/no)',
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

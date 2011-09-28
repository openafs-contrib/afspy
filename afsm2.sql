SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `afsm2` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `afsm2` ;

-- -----------------------------------------------------
-- Table `afsm2`.`tbl_cells`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_cells` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL DEFAULT 'none' ,
  `maxuser` INT(11)  NULL DEFAULT 0 ,
  `maxgroup` INT(11)  NULL DEFAULT 0 ,
  `description` TEXT NULL DEFAULT NULL ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
COMMENT = 'AFS CELL';

CREATE UNIQUE INDEX `idx_name` ON `afsm2`.`tbl_cells` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_locations`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_locations` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `location_type` TEXT NULL ,
  `gps` TEXT NULL ,
  `country` TEXT NULL ,
  `city` TEXT NULL ,
  `street` TEXT NULL ,
  `pobox` TEXT NULL ,
  `description` TEXT NULL ,
  `ldate` INT(11)  NOT NULL ,
  `cdate` INT(11)  NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

CREATE UNIQUE INDEX `idx_name` ON `afsm2`.`tbl_locations` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_entities`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_entities` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `entity_type` TEXT NOT NULL ,
  `entity_father` TEXT NULL ,
  `address` TEXT NULL ,
  `contact` TEXT NULL ,
  `description` TEXT NULL ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_entities` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_identities`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_identities` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `identity_type` INT(11)  NOT NULL ,
  `entity_name` TEXT NOT NULL ,
  `contact` TEXT NULL ,
  `description` TEXT NULL ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `name`
    FOREIGN KEY (`entity_name` )
    REFERENCES `afsm2`.`tbl_entities` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_identities` (`name` ASC) ;

CREATE INDEX `idx_entity_name` ON `afsm2`.`tbl_identities` (`entity_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_costcenters`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_costcenters` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `identity_name` TEXT NOT NULL ,
  `description` TEXT NULL ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `identity_name`
    FOREIGN KEY (`identity_name` )
    REFERENCES `afsm2`.`tbl_identities` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_costcenters` (`name` ASC) ;

CREATE INDEX `identity_name` ON `afsm2`.`tbl_costcenters` (`identity_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_servers`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_servers` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NULL ,
  `server_type` TEXT NULL ,
  `localtion_name` TEXT NULL ,
  `owner` TEXT NULL ,
  `administrator` TEXT NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `entity`
    FOREIGN KEY (`owner` )
    REFERENCES `afsm2`.`tbl_entities` (`name` )
    ON DELETE SET NULL
    ON UPDATE RESTRICT,
  CONSTRAINT `identity`
    FOREIGN KEY (`administrator` )
    REFERENCES `afsm2`.`tbl_identities` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `location_name`
    FOREIGN KEY (`localtion_name` )
    REFERENCES `afsm2`.`tbl_locations` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_servers` (`name` ASC) ;

CREATE INDEX `entity` ON `afsm2`.`tbl_servers` (`owner` ASC) ;

CREATE INDEX `identity` ON `afsm2`.`tbl_servers` (`administrator` ASC) ;

CREATE INDEX `location_name` ON `afsm2`.`tbl_servers` (`localtion_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_afsmuser`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_afsmuser` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `password` TEXT NULL ,
  `email` TEXT NULL ,
  `description` TEXT NULL ,
  `lastaccess` INT(11)  NULL ,
  `pwd_expiried` INT(11)  NULL ,
  `status` INT(11)  NULL ,
  `udate` INT(11)  NULL DEFAULT 0 ,
  `cdate` INT(11)  NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_afsmuser` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_afs_servers`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_afs_servers` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `cell_name` TEXT NULL ,
  `uuid` TEXT NULL ,
  `arch` TEXT NULL ,
  `afsip` TEXT NULL ,
  `fileserver` INT(11)  NULL DEFAULT 0 ,
  `dbserver` INT(11)  NULL DEFAULT 0 ,
  `confserver` INT(11)  NULL DEFAULT 0 ,
  `distserver` INT(11)  NULL DEFAULT 0 ,
  `afs_class` TEXT NULL DEFAULT 0 ,
  `afsserver_status` TEXT NULL DEFAULT 0 ,
  `location_name` TEXT NULL ,
  `sync` INT(11)  NULL ,
  `description` TEXT NULL ,
  `admin` TEXT NULL ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `name`
    FOREIGN KEY (`name` )
    REFERENCES `afsm2`.`tbl_servers` (`name` )
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `admin`
    FOREIGN KEY (`admin` )
    REFERENCES `afsm2`.`tbl_afsmuser` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `name` ON `afsm2`.`tbl_afs_servers` (`name` ASC) ;

CREATE INDEX `admin` ON `afsm2`.`tbl_afs_servers` (`admin` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_server_hw`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_server_hw` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `server_id` INT(11)  NOT NULL ,
  `elem_class` INT(11)  NOT NULL ,
  `elem_seq` INT(11)  NOT NULL ,
  `item_type` VARCHAR(45) NULL ,
  `item_value` TEXT NULL ,
  `description` TEXT NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `id`
    FOREIGN KEY (`server_id` )
    REFERENCES `afsm2`.`tbl_servers` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `inx_srv_class` ON `afsm2`.`tbl_server_hw` (`server_id` ASC, `elem_class` ASC) ;

CREATE INDEX `id` ON `afsm2`.`tbl_server_hw` (`server_id` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_partitions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_partitions` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `partition_name` TEXT NOT NULL ,
  `server_name` TEXT NOT NULL ,
  `part_class` TEXT NULL ,
  `size` INT(11)  NULL ,
  `free` INT(11)  NULL ,
  `perc` INT(11)  NULL ,
  `description` INT(11)  NULL ,
  `sync` INT(11)  NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `server_name`
    FOREIGN KEY (`server_name` )
    REFERENCES `afsm2`.`tbl_servers` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `idx_server` ON `afsm2`.`tbl_partitions` (`server_name` ASC) ;

CREATE INDEX `server_name` ON `afsm2`.`tbl_partitions` (`server_name` ASC) ;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_partitions` (`name` ASC) ;

CREATE UNIQUE INDEX `pk_srv_part` ON `afsm2`.`tbl_partitions` (`partition_name` ASC, `server_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`lnk_server_hw_parttion`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`lnk_server_hw_parttion` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `server_hw_id` INT(11)  NULL ,
  `partition_id` INT(11)  NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `server_id`
    FOREIGN KEY (`server_hw_id` )
    REFERENCES `afsm2`.`tbl_server_hw` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `partition_id`
    FOREIGN KEY (`partition_id` )
    REFERENCES `afsm2`.`tbl_partitions` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `server_id` ON `afsm2`.`lnk_server_hw_parttion` (`server_hw_id` ASC) ;

CREATE INDEX `partition_id` ON `afsm2`.`lnk_server_hw_parttion` (`partition_id` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_instance`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_instance` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `server_name` TEXT NOT NULL ,
  `process_name` TEXT NOT NULL ,
  `status` TEXT NULL ,
  `cell_name` TEXT NULL ,
  `startdate` TEXT NULL ,
  `startcount` TEXT NULL ,
  `exitdate` TEXT NULL ,
  `notifier` TEXT NULL ,
  `state` TEXT NULL ,
  `errorstop` TEXT NULL ,
  `core` TEXT NULL ,
  `errorexitdate` TEXT NULL ,
  `errorexitdue` TEXT NULL ,
  `errorexistsignal` TEXT NULL ,
  `errorexitcode` TEXT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `server_name`
    FOREIGN KEY (`server_name` )
    REFERENCES `afsm2`.`tbl_servers` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_instance` (`name` ASC) ;

CREATE INDEX `server_name` ON `afsm2`.`tbl_instance` (`server_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_volumes`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_volumes` (
  `id` INT(11)  NOT NULL ,
  `name` TEXT NOT NULL ,
  `server_name` TEXT NOT NULL ,
  `partition_name` TEXT NOT NULL ,
  `cell_name` TEXT NULL ,
  `vtype` TEXT NULL ,
  `size` INT(11)  NULL DEFAULT 0 ,
  `maxquota` INT(11)  NULL DEFAULT 0 ,
  `id_parent` INT(11)  NULL DEFAULT 0 ,
  `status` TEXT NULL ,
  `attached` TEXT NULL ,
  `fcount` INT(11)  NULL DEFAULT 0 ,
  `rocount` INT(11)  NULL DEFAULT 0 ,
  `duse` INT(11)  NULL DEFAULT 0 ,
  `inuse` TEXT NULL ,
  `afscreation` TEXT NULL ,
  `afsupdate` TEXT NULL ,
  `perc` FLOAT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `ldate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `server_name`
    FOREIGN KEY (`server_name` , `partition_name` )
    REFERENCES `afsm2`.`tbl_partitions` (`server_name` , `partition_name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `idx_server_name` ON `afsm2`.`tbl_volumes` (`server_name` ASC) ;

CREATE INDEX `idx_afsupdate` ON `afsm2`.`tbl_volumes` (`afsupdate` ASC) ;

CREATE INDEX `server_name` ON `afsm2`.`tbl_volumes` (`server_name` ASC, `partition_name` ASC) ;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_volumes` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_volume_extras`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_volume_extras` (
  `id` INT(11)  NOT NULL ,
  `fquota` INT(11)  NULL DEFAULT 0 ,
  `blockfs` INT(11)  NULL DEFAULT 0 ,
  `block_osd_on` INT(11)  NULL DEFAULT 0 ,
  `block_osd_off` INT(11)  NULL DEFAULT 0 ,
  `pinned` INT(11)  NULL DEFAULT 0 ,
  `edate` INT(11)  NULL DEFAULT 0 ,
  `mincopy` INT(11)  NULL DEFAULT 0 ,
  `osdpolicy` INT(11)  NULL DEFAULT 0 ,
  `owner` TEXT NULL DEFAULT 'none' ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `id`
    FOREIGN KEY (`id` )
    REFERENCES `afsm2`.`tbl_volumes` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner` )
    REFERENCES `afsm2`.`tbl_identities` (`name` )
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `owner` ON `afsm2`.`tbl_volume_extras` (`owner` ASC) ;

CREATE INDEX `owner` ON `afsm2`.`tbl_volume_extras` (`owner` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_volume_groups`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_volume_groups` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `regex` TEXT NULL DEFAULT '' ,
  `group_class` TEXT NULL DEFAULT 'none' ,
  `minsize` INT(11)  NULL DEFAULT 0 ,
  `maxsize` INT(11)  NULL DEFAULT 0 ,
  `description` TEXT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_volume_groups` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`lnk_volume_group`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`lnk_volume_group` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `volume_group_id` INT(11)  NULL ,
  `volume_id` INT(11)  NULL ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `volume_group_id`
    FOREIGN KEY (`volume_group_id` )
    REFERENCES `afsm2`.`tbl_volume_groups` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `volume_id`
    FOREIGN KEY (`volume_id` )
    REFERENCES `afsm2`.`tbl_volumes` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = 'Link Table Volumes Volume Group';

CREATE INDEX `volume_group_id` ON `afsm2`.`lnk_volume_group` (`volume_group_id` ASC) ;

CREATE INDEX `volume_id` ON `afsm2`.`lnk_volume_group` (`volume_id` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_projects`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_projects` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NOT NULL ,
  `volume_group_name` TEXT NULL ,
  `owner` TEXT NULL ,
  `entity_name` TEXT NULL ,
  `primary_rw` TEXT NULL DEFAULT 'none' ,
  `primary_ro` TEXT NULL DEFAULT 'none' ,
  `rwspid` TEXT NULL DEFAULT 'none' ,
  `rospid` TEXT NULL DEFAULT 'none' ,
  `maxsize` INT(11)  NULL ,
  `costcenter` TEXT NULL ,
  `description` TEXT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `rw_location`
    FOREIGN KEY (`primary_rw` )
    REFERENCES `afsm2`.`tbl_locations` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `ro_location`
    FOREIGN KEY (`primary_ro` )
    REFERENCES `afsm2`.`tbl_locations` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner` )
    REFERENCES `afsm2`.`tbl_identities` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `volume_group`
    FOREIGN KEY (`volume_group_name` )
    REFERENCES `afsm2`.`tbl_volume_groups` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `costcenter`
    FOREIGN KEY (`costcenter` )
    REFERENCES `afsm2`.`tbl_costcenters` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `entity_name`
    FOREIGN KEY (`entity_name` )
    REFERENCES `afsm2`.`tbl_entities` (`name` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_projects` (`name` ASC) ;

CREATE INDEX `rw_location` ON `afsm2`.`tbl_projects` (`primary_rw` ASC) ;

CREATE INDEX `ro_location` ON `afsm2`.`tbl_projects` (`primary_ro` ASC) ;

CREATE INDEX `owner` ON `afsm2`.`tbl_projects` (`owner` ASC) ;

CREATE INDEX `volume_group` ON `afsm2`.`tbl_projects` (`volume_group_name` ASC) ;

CREATE INDEX `costcenter` ON `afsm2`.`tbl_projects` (`costcenter` ASC) ;

CREATE INDEX `entity_name` ON `afsm2`.`tbl_projects` (`entity_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_mount_points`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_mount_points` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `volume_name` TEXT NOT NULL ,
  `path` TEXT NOT NULL ,
  `name` TEXT NOT NULL ,
  `symlink` INT(11)  NULL ,
  `rw` INT(11)  NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `volume_name`
    FOREIGN KEY (`volume_name` )
    REFERENCES `afsm2`.`tbl_volumes` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `afsm2`.`tbl_mount_points` (`name` ASC) ;

CREATE INDEX `volume_name` ON `afsm2`.`tbl_mount_points` (`volume_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_volume_stats`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_volume_stats` (
  `id` INT(11)  NOT NULL ,
  `read_same_total` INT(11)  NULL DEFAULT 0 ,
  `read_some_auth` INT(11)  NULL DEFAULT 0 ,
  `write_some_total` INT(11)  NULL DEFAULT 0 ,
  `write_some_auth` INT(11)  NULL DEFAULT 0 ,
  `read_diff_total` INT(11)  NULL DEFAULT 0 ,
  `read_diff_auth` INT(11)  NULL DEFAULT 0 ,
  `write_diff_total` INT(11)  NULL DEFAULT 0 ,
  `write_diff_auth` INT(11)  NULL DEFAULT 0 ,
  `author_1day_dir_same` INT(11)  NULL DEFAULT 0 ,
  `author_1wk_dir_same` INT(11)  NULL DEFAULT 0 ,
  `author_1day_dir_diff` INT(11)  NULL DEFAULT 0 ,
  `author_1wk_dir_diff` INT(11)  NULL DEFAULT 0 ,
  `author_1day_file_same` INT(11)  NULL DEFAULT 0 ,
  `author_1wk_file_same` INT(11)  NULL DEFAULT 0 ,
  `author_1day_file_diff` INT(11)  NULL DEFAULT 0 ,
  `author_1wk_file_diff` INT(11)  NULL DEFAULT 0 ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `volume_id`
    FOREIGN KEY (`id` )
    REFERENCES `afsm2`.`tbl_volumes` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `volume_id` ON `afsm2`.`tbl_volume_stats` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_users` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `name` TEXT NULL ,
  `max_space` INT(11)  NULL DEFAULT 0 ,
  `max_volume` INT(11)  NULL DEFAULT 0 ,
  `user_type` TEXT NULL ,
  `account_expires` INT(11)  NULL DEFAULT 0 ,
  `password_expires` INT(11)  NULL DEFAULT 0 ,
  `description` TEXT NULL ,
  `email` TEXT NULL ,
  `entity_name` TEXT NULL ,
  `udate` INT(11)  NULL DEFAULT 0 ,
  `cdate` INT(11)  NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `items`
    FOREIGN KEY (`entity_name` )
    REFERENCES `afsm2`.`tbl_entities` (`name` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `items` ON `afsm2`.`tbl_users` (`entity_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_afsusers`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_afsusers` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `afsid` INT(11)  NOT NULL ,
  `name` TEXT NULL ,
  `owner` TEXT NULL ,
  `creator` TEXT NULL ,
  `quota` INT(11)  NULL ,
  `flag1` TEXT NULL ,
  `flag2` TEXT NULL ,
  `flag3` TEXT NULL ,
  `flag4` TEXT NULL ,
  `flag5` TEXT NULL ,
  `afsuser_type` TEXT NULL ,
  `kvno` INT(11)  NULL ,
  `realm` INT(11)  NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `user_id`
    FOREIGN KEY (`id` )
    REFERENCES `afsm2`.`tbl_users` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `afsid_UNIQUE` ON `afsm2`.`tbl_afsusers` (`afsid` ASC) ;

CREATE INDEX `user_id` ON `afsm2`.`tbl_afsusers` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`lnk_afsuser`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`lnk_afsuser` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `afsgroup` INT(11)  NOT NULL ,
  `afsmember` INT(11)  NOT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NULL DEFAULT 0 ,
  `cdate` INT(11)  NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `afsgroup`
    FOREIGN KEY (`afsgroup` )
    REFERENCES `afsm2`.`tbl_afsusers` (`afsid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `afsmember`
    FOREIGN KEY (`afsmember` )
    REFERENCES `afsm2`.`tbl_afsusers` (`afsid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `afsgroup` ON `afsm2`.`lnk_afsuser` (`afsgroup` ASC) ;

CREATE INDEX `afsmember` ON `afsm2`.`lnk_afsuser` (`afsmember` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_transactions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_transactions` (
  `id` INT(11)  NOT NULL ,
  `server_name` TEXT NULL ,
  `created` TEXT NULL ,
  `attach_flags` TEXT NULL ,
  `volume` TEXT NULL ,
  `partition` TEXT NULL ,
  `procedure` TEXT NULL ,
  `packet_read` TEXT NULL ,
  `last_receive_time` TEXT NULL ,
  `packet_send` TEXT NULL ,
  `last_send_time` TEXT NULL ,
  `sync` INT(11)  NULL DEFAULT 0 ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `server_name`
    FOREIGN KEY (`server_name` )
    REFERENCES `afsm2`.`tbl_servers` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `idx_server_name` ON `afsm2`.`tbl_transactions` (`server_name` ASC) ;

CREATE INDEX `server_name` ON `afsm2`.`tbl_transactions` (`server_name` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_jobs`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_jobs` (
  `id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `job_type` TEXT NULL ,
  `command` TEXT NULL ,
  `owner` TEXT NULL ,
  `schedule` TEXT NULL ,
  `description` TEXT NULL ,
  `result` TEXT NULL ,
  `status` TEXT NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner` )
    REFERENCES `afsm2`.`tbl_afsmuser` (`name` )
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `owner` ON `afsm2`.`tbl_jobs` (`owner` ASC) ;


-- -----------------------------------------------------
-- Table `afsm2`.`tbl_logs`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `afsm2`.`tbl_logs` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `session` TEXT NULL ,
  `transaction` TEXT NULL ,
  `service` TEXT NULL ,
  `param` TEXT NULL ,
  `action` TEXT NULL ,
  `subcmd` TEXT NULL ,
  `owner` TEXT NULL ,
  `host` TEXT NULL ,
  `udate` INT(11)  NOT NULL DEFAULT 0 ,
  `cdate` INT(11)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner` )
    REFERENCES `afsm2`.`tbl_afsmuser` (`name` )
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `owner` ON `afsm2`.`tbl_logs` (`owner` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

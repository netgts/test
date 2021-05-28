-- --------------------------------------------------------
-- Хост:                         localhost
-- Версия сервера:               5.5.62 - MySQL Community Server (GPL)
-- Операционная система:         Win64
-- HeidiSQL Версия:              11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE DATABASE IF NOT EXISTS `devices` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `devices`;


CREATE TABLE IF NOT EXISTS `equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial_num` varchar(15) NOT NULL DEFAULT '',
  `id_equip` int(11) NOT NULL COMMENT 'Код типа оборудования',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `Serial_num_2` (`serial_num`) USING BTREE,
  KEY `FK_equipment_type_equip` (`id_equip`),
  CONSTRAINT `FK_equipment_type_equip` FOREIGN KEY (`id_equip`) REFERENCES `type_equip` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;


-- Дамп структуры для таблица devices.type_equip
CREATE TABLE IF NOT EXISTS `type_equip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_equip` varchar(50) NOT NULL,
  `sn_mask` varchar(15) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

INSERT INTO `type_equip` (`id`, `name_equip`, `sn_mask`) VALUES
	(1, 'TP-Link TL-WR74', 'XXAAAAAXAA'),
	(2, 'D-Link DIR-300', 'NXXAAXZXaa'),
	(3, 'D-Link DIR-300 S', 'NXXAAXZXXX');
	
CREATE USER 'developer'@'localhost' IDENTIFIED BY '111';
GRANT ALL PRIVILEGES ON *.* TO 'developer'@'localhost' WITH GRANT OPTION;	
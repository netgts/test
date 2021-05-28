CREATE DATABASE IF NOT EXISTS `devices`;
USE `devices`;


CREATE TABLE IF NOT EXISTS `equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial_num` varchar(15) NOT NULL DEFAULT '',
  `id_equip` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `Serial_num_2` (`serial_num`) USING BTREE,
  KEY `FK_equipment_type_equip` (`id_equip`),
  CONSTRAINT `FK_equipment_type_equip` FOREIGN KEY (`id_equip`) REFERENCES `type_equip` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;



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
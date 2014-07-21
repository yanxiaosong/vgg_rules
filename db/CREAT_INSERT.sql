-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.14 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table vgg.order
CREATE TABLE IF NOT EXISTS `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL,
  `regular_price` int(11) DEFAULT '0' COMMENT 'order price before promotion',
  `actual_price` int(11) DEFAULT '0' COMMENT 'order price after pormotion',
  `status` int(11) DEFAULT '0' COMMENT '0: new; 1: checkout',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=utf8;


-- Dumping structure for table vgg.order_detail
CREATE TABLE IF NOT EXISTS `order_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `amount` mediumint(9) NOT NULL,
  `unit_price` int(11) NOT NULL,
  `regular_price` int(11) NOT NULL COMMENT 'total price before promotion',
  `actual_price` int(11) DEFAULT '0' COMMENT 'actual price after promotion',
  PRIMARY KEY (`id`),
  KEY `fk_product` (`product_id`),
  KEY `FK2_order` (`order_id`),
  CONSTRAINT `FK2_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `fk_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=531 DEFAULT CHARSET=utf8;


-- Dumping structure for table vgg.order_promotion_log
CREATE TABLE IF NOT EXISTS `order_promotion_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `promotion_id` int(11) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `order_detail_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `promotion_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK1_promotion` (`promotion_id`),
  KEY `FK2_promo_log_order` (`order_id`),
  KEY `FK3_promo_log_order_detail` (`order_detail_id`),
  CONSTRAINT `FK3_promo_log_order_detail` FOREIGN KEY (`order_detail_id`) REFERENCES `order_detail` (`id`),
  CONSTRAINT `FK1_promotion` FOREIGN KEY (`promotion_id`) REFERENCES `promotion` (`id`),
  CONSTRAINT `FK2_promo_log_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;


-- Dumping structure for table vgg.product
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `status` int(11) NOT NULL COMMENT '1: active; 0: not active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`product_code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Dumping data for table vgg.product: ~4 rows (approximately)
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` (`id`, `product_code`, `name`, `price`, `status`) VALUES
	(1, 'APPLE', 'red apple', 100, 1),
	(2, 'ORANGE', 'big orange', 200, 1),
	(3, 'PEAR', 'green pear ', 150, 1),
	(4, 'BLBRRY', 'blue berry', 500, 1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;


-- Dumping structure for table vgg.promotion
CREATE TABLE IF NOT EXISTS `promotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `rule_script` text NOT NULL,
  `description` varchar(500) NOT NULL,
  `status` tinyint(4) NOT NULL COMMENT '0: not active; 1: active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Dumping data for table vgg.promotion: ~0 rows (approximately)
/*!40000 ALTER TABLE `promotion` DISABLE KEYS */;
INSERT INTO `promotion` (`id`, `code`, `rule_script`, `description`, `status`) VALUES
	(1, 'APPLE2_1', '{ "conditions": { "all": [\r\n      { "name": "product_code",\r\n        "operator": "equal_to",\r\n        "value": "APPLE"\r\n      },\r\n      { "name": "product_amount",\r\n        "operator": "greater_than_or_equal_to",\r\n        "value": 5\r\n      }\r\n  ]},\r\n  "actions": [\r\n      { "name": "buy_and_get_cheaper",\r\n        "params": {"buy_count": 5,  "cheaper_count": 2, "sale_percentage": 0}\r\n      }\r\n  ]\r\n}', 'Buy 5 apple, get 2 free', 1),
	(2, 'ORANGE_3', '{ "conditions": { "all": [\r\n      { "name": "product_code",\r\n        "operator": "equal_to",\r\n        "value": "ORANGE"\r\n      },\r\n      { "name": "product_amount",\r\n        "operator": "greater_than_or_equal_to",\r\n        "value": 3\r\n      }\r\n  ]},\r\n  "actions": [\r\n      { "name": "buy_group_and_cheaper",\r\n        "params": {"group_count": 3,  "sale_price": 180}\r\n      }\r\n  ]\r\n}', 'Buy 3 oranges in a group at price $1.80 each(10% off)', 1);
/*!40000 ALTER TABLE `promotion` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

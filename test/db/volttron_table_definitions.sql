DROP TABLE IF EXISTS `volttron_table_definitions`;

CREATE TABLE `volttron_table_definitions` (
  `table_id` varchar(512) NOT NULL,
  `table_name` varchar(512) NOT NULL,
  `table_prefix` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`table_id`)
);

INSERT INTO `volttron_table_definitions` VALUES ('data_table','data',''),('meta_table','meta',''),('topics_table','topics','');

/*
SQLyog Community v13.0.0 (64 bit)
MySQL - 10.1.21-MariaDB : Database - ppsi
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`ppsi` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ppsi`;

/*Table structure for table `th_review` */

DROP TABLE IF EXISTS `th_review`;

CREATE TABLE `th_review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_event` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `date_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `th_review` */

insert  into `th_review`(`id`,`id_event`,`id_user`,`comment`,`date_time`) values 
(1,2,1,'Terbaik Bos','2018-06-26 20:35:46');

/*Table structure for table `tm_category` */

DROP TABLE IF EXISTS `tm_category`;

CREATE TABLE `tm_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(200) DEFAULT NULL,
  `status` char(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tm_category` */

insert  into `tm_category`(`id`,`category_name`,`status`) values 
(1,'Sport','00'),
(2,'Music','00'),
(3,'Game','00'),
(4,'Art','00'),
(5,'Fiction','00');

/*Table structure for table `tm_event` */

DROP TABLE IF EXISTS `tm_event`;

CREATE TABLE `tm_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) DEFAULT NULL,
  `province` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `date_from` date DEFAULT NULL,
  `date_to` date DEFAULT NULL,
  `time_from` time DEFAULT NULL,
  `time_to` time DEFAULT NULL,
  `price_before` varchar(200) DEFAULT NULL,
  `price` varchar(200) DEFAULT NULL,
  `status` char(2) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `id_category` int(1) DEFAULT NULL,
  `max_join` char(4) DEFAULT NULL,
  `register_needed` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `tm_event` */

insert  into `tm_event`(`id`,`id_user`,`province`,`city`,`title`,`date_from`,`date_to`,`time_from`,`time_to`,`price_before`,`price`,`status`,`gender`,`id_category`,`max_join`,`register_needed`) values 
(2,1,'DKI Jakarta','Jakarta Pusat','Java Jazz 2018','2018-06-26','2018-06-29','12:00:00','15:00:00','20K','100K','00','a',1,'200','1'),
(6,1,'DKI Jakarta','Malang','Turnament baiduri sepah','2017-12-12','2018-12-12','12:00:00','15:00:00','20.000','280.000.000','00','a',1,'12','0');

/*Table structure for table `tm_user` */

DROP TABLE IF EXISTS `tm_user`;

CREATE TABLE `tm_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(25) DEFAULT NULL,
  `mobile` varchar(13) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `status` char(2) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `image_uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tm_user` */

insert  into `tm_user`(`id`,`first_name`,`last_name`,`email`,`mobile`,`password`,`status`,`gender`,`image_uri`) values 
(1,'herdian','bagus','dianbagus96@gmail.com','082331012511','569800','00','M','/static/assets/testimonials/xChris29-a1c50b45ebd1e6038a79359610d672d9f803b34b682e838b832b500223cbfaa5.png.pagespeed.ic.c5BXLyfx-O.jpg'),
(2,'Firdha','Imamah','firdhaimamah@gmail.com','082331012511','569800','00','f','/static/assets/testimonials/xChris29-a1c50b45ebd1e6038a79359610d672d9f803b34b682e838b832b500223cbfaa5.png.pagespeed.ic.c5BXLyfx-O.jpg');

/*Table structure for table `tx_participants` */

DROP TABLE IF EXISTS `tx_participants`;

CREATE TABLE `tx_participants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_event` int(11) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mobile` varchar(13) DEFAULT NULL,
  `no_eticket` varchar(255) DEFAULT NULL,
  `date_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` char(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `tx_participants` */

insert  into `tx_participants`(`id`,`id_event`,`first_name`,`last_name`,`email`,`mobile`,`no_eticket`,`date_time`,`status`) values 
(6,1,'herdian','bagus','dianbagus96@gmail.com','082331012511',NULL,'2018-06-26 22:39:13','00'),
(10,2,'faiz','faizdwi','faiztelkom@gmail.com','082331012511',NULL,'2018-06-27 19:11:22','00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

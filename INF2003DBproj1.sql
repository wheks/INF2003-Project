/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.5.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: inf2003proj1
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `airlines`
--

DROP TABLE IF EXISTS `airlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `airlines` (
  `aid` varchar(50) NOT NULL,
  `acount` int(11) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airlines`
--

LOCK TABLES `airlines` WRITE;
/*!40000 ALTER TABLE `airlines` DISABLE KEYS */;
INSERT INTO `airlines` VALUES
('Airasia',6),
('Malaysia Airline',7),
('Scoot',10),
('Singapore Airlines',17),
('Thai Airways',7),
('Vietjet',8);
/*!40000 ALTER TABLE `airlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `countries` (
  `cid` varchar(50) NOT NULL,
  `ccount` int(11) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES
('Brunei',4),
('Cambodia',3),
('Indonesia',8),
('Laos',1),
('Malaysia',4),
('Myanmar',2),
('Philippines',9),
('Thailand',10),
('Timor Leste',1),
('Vietnam',13);
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `length_of_stay`
--

DROP TABLE IF EXISTS `length_of_stay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `length_of_stay` (
  `lid` varchar(50) NOT NULL,
  `loscount` int(11) DEFAULT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `length_of_stay`
--

LOCK TABLES `length_of_stay` WRITE;
/*!40000 ALTER TABLE `length_of_stay` DISABLE KEYS */;
INSERT INTO `length_of_stay` VALUES
('10_to_12',5),
('1_to_3',27),
('4_to_6',13),
('7_to_9',4),
('>12',6);
/*!40000 ALTER TABLE `length_of_stay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passenger` (
  `pid` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `lid` varchar(50) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Gender` varchar(3) DEFAULT NULL,
  `aid` varchar(50) DEFAULT NULL,
  `cid` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `fk_passenger_lid` (`lid`),
  KEY `fk_passenger_aid` (`aid`),
  KEY `fk_passenger_cid` (`cid`),
  CONSTRAINT `fk_passenger_aid` FOREIGN KEY (`aid`) REFERENCES `airlines` (`aid`),
  CONSTRAINT `fk_passenger_cid` FOREIGN KEY (`cid`) REFERENCES `countries` (`cid`),
  CONSTRAINT `fk_passenger_lid` FOREIGN KEY (`lid`) REFERENCES `length_of_stay` (`lid`),
  CONSTRAINT `chk_age` CHECK (`Age` >= 0 and `Age` <= 130)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES
(1,'Li Wei','4_to_6',32,'M','Singapore Airlines','Malaysia'),
(2,'Zhang Xin ','4_to_6',42,'M','Scoot','Malaysia'),
(3,'Adeline Lim','1_to_3',29,'F','Scoot','Vietnam'),
(4,'Priya Patel','4_to_6',31,'F','Airasia','Indonesia'),
(5,'Zhang Wei','1_to_3',50,'M','Scoot','Indonesia'),
(6,'Rina','1_to_3',26,'M','Singapore Airlines','Indonesia'),
(7,'Liana Brasales','1_to_3',25,'F','Airasia','Indonesia'),
(8,'Ananya Sharma','4_to_6',33,'F','Vietjet','Vietnam'),
(9,'Nguyen Van Minh','1_to_3',45,'M','Vietjet','Vietnam'),
(10,'Mei Ling','4_to_6',29,'F','Thai Airways','Thailand'),
(11,'Arjun Singh','1_to_3',32,'M','Thai AIrways','Thailand'),
(12,'Siti Nurhayat','4_to_6',27,'F','Singapore Airlines','Thailand'),
(13,'Seok Hui','>12',56,'F','Malaysia Airline','Malaysia'),
(14,'Zheng Hua','1_to_3',24,'M','Scoot','Laos'),
(15,'Joshua Ng','1_to_3',29,'M','Scoot','Myanmar'),
(16,'Bryan Wee','1_to_3',6,'NB','Airasia','Brunei'),
(17,'Markas Lee','10 to 12',21,'M','Scoot','Cambodia'),
(18,'David Philip Matthew','10 to 12',72,'NB','Malaysia Airline','Timor Leste'),
(19,'Crystal Seow','7_to_9 ',18,'F','Scoot','Philippines'),
(20,'Michael Jordan','>12',56,'M','Singapore Airlines','Philippines'),
(21,'Nguyen Thi Linh','1_to_3',24,'F','Vietjet','Vietnam'),
(22,'Supachai Rattanasupa','>12',57,'M','Thai Airways','Thailand'),
(23,'Muhammad Rizal bin Abdullah','7_to_9 ',33,'M','Singapore Airlines','Brunei'),
(24,'Tran Van Minh','1_to_3',19,'F','Vietjet','Vietnam'),
(25,'Siti Nurhayati','1_to_3',42,'F','Singapore Airlines','Indonesia'),
(26,'Apinya Charoenphon','7_to_9 ',68,'F','Thai Airways','Thailand'),
(27,'Le Thi Hoa','1_to_3',29,'F','Singapore Airlines','Vietnam'),
(28,'Arief Wicaksono','7_to_9 ',51,'M','Scoot','Philippines'),
(29,'Maria Corazon de la Cruz','4_to_6',36,'F','Scoot','Philippines'),
(30,'Pham Duc Anh','1_to_3',22,'M','Singapore Airlines','Vietnam'),
(31,'Nattapong Jaidee','4_to_6',45,'M','Thai Airways','Thailand'),
(32,'Nurul Aini binti Yusof','>12',61,'F','Singapore Airlines','Indonesia'),
(33,'Dang Quoc Hung','4_to_6',27,'F','Vietjet','Vietnam'),
(34,'Kannika Srisawat','1_to_3',39,'M','Airasia','Thailand'),
(35,'Jose Ramon Santos','1_to_3',53,'M','Singapore Airlines','Philippines'),
(36,'Vo Thi Thanh','4_to_6',31,'M','Vietjet','Vietnam'),
(37,'Bambang Suparno','10 to 12',48,'M','Singapore Airlines','Indonesia'),
(38,'Malia Andrada','1_to_3',72,'F','Singapore Airlines','Philippines'),
(39,'Nguyen Van Hieu','4_to_6',25,'F','Vietjet','Vietnam'),
(40,'Ratana Chhay','4_to_6',59,'F','Singapore Airlines','Malaysia'),
(41,'Zain Azmi bin Ismail','1_to_3',34,'M','Malaysia Airline','Brunei'),
(42,'Hoang Thi Mai','4_to_6',47,'M','Vietjet','Vietnam'),
(43,'Suthatip Ratanaporn','1_to_3',20,'M','Thai Airways','Thailand'),
(44,'Ernesto Bautista III','10 to 12',63,'M','Singapore Airlines','Philippines'),
(45,'Tran Duc Thang','1_to_3',38,'M','Singapore Airlines','Vietnam'),
(46,'Dewi Lestari','>12',55,'F','Scoot','Philippines'),
(47,'Chanthavong Sisoulith','1_to_3',41,'NB','Thai Airways','Thailand'),
(48,'Nguyen Thi Quynh Anh','1_to_3',28,'F','Airasia','Vietnam'),
(49,'Pradit Phongphaiboun','>12',66,'NB','Airasia','Thailand'),
(50,'Mariam binti Osman','1_to_3',43,'F','Malaysia Airline','Indonesia'),
(51,'Mike Tyson','1_to_3',88,'M','Singapore Airlines','Philippines'),
(52,'Shi Yu','1_to_3',20,'NB','Malaysia Airline','Myanmar'),
(53,'Tom','1_to_3',12,'F','Malaysia Airline','Cambodia'),
(54,'Tom','1_to_3',12,'F','Malaysia Airline','Cambodia'),
(55,'Sam','10_to_12',12,'M','Singapore Airlines','Brunei');
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-10-11 22:22:49

-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: classroom_server
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` varchar(10) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('a_1','1234'),('a_2','1234'),('a_3','1234'),('a_4','1234');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assigned_teacher`
--

DROP TABLE IF EXISTS `assigned_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assigned_teacher` (
  `teacher_id` varchar(20) DEFAULT NULL,
  `course_id` varchar(10) DEFAULT NULL,
  `section` varchar(2) DEFAULT NULL,
  `intake` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned_teacher`
--

LOCK TABLES `assigned_teacher` WRITE;
/*!40000 ALTER TABLE `assigned_teacher` DISABLE KEYS */;
INSERT INTO `assigned_teacher` VALUES ('t_1','MAT231','7','53'),('t_2','CSE231','7','53'),('t_2','CSE232','7','53'),('t_3','CSE207','7','53'),('t_3','CSE208','7','53'),('t_4','CSE209','7','53'),('t_4','CSE210','7','53'),('t_5','CSE215','7','53');
/*!40000 ALTER TABLE `assigned_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `id` varchar(10) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `mac` varchar(20) DEFAULT NULL,
  `intake` varchar(5) DEFAULT NULL,
  `section` varchar(3) DEFAULT NULL,
  `department` varchar(30) DEFAULT NULL,
  `present_ping` varchar(3) DEFAULT NULL,
  `total_ping` varchar(3) DEFAULT NULL,
  `percentage` varchar(10) DEFAULT NULL,
  `state` varchar(10) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `period_no` varchar(3) DEFAULT NULL,
  `course_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','2',NULL,'present','2025-10-11','4','CSE215'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2',NULL,'absent','2025-10-11','4','CSE215'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','2','2',NULL,'absent','2025-10-11','5','CSE207'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2',NULL,'absent','2025-10-11','5','CSE207'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','2','2','1','present','2025-10-11','6','CSE215'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','6','CSE215'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','3','4','75','present','2025-10-11','3','CSE209'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','4','0','absent','2025-10-11','3','CSE209'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','0','2','0','present','2025-10-11','6','CSE215'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','2','50','present','2025-10-11','6','CSE215'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','6','CSE215'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','7','CSE231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','2','2','100','present','2025-10-11','7','CSE231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','7','CSE231'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','8','CSE232'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','2','50','absent','2025-10-11','8','CSE232'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','8','CSE232'),('st_3','test_student','90:78:b2:ce:71:63','53','7','Mathematics','2','2','100','present','2025-10-11','1','MAT231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','Mathematics','2','2','100','present','2025-10-11','1','MAT231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','Mathematics','0','2','0','absent','2025-10-11','1','MAT231'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','2','CSE231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','2','50','absent','2025-10-11','2','CSE231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','2','CSE231'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','3','CSE209'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','absent','2025-10-11','3','CSE209'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','3','CSE209'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','4','CSE215'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','present','2025-10-11','4','CSE215'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','4','CSE215'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','1','2','50','present','2025-10-11','6','CSE215'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','2','50','present','2025-10-11','6','CSE215'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','6','CSE215'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-11','7','CSE231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','2','2','100','present','2025-10-11','7','CSE231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-11','7','CSE231'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','0','2','0','absent','2025-10-12','7','CSE232'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','absent','2025-10-12','7','CSE232'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-12','7','CSE232'),('st_3','test_student','90:78:b2:ce:71:63','53','7','Mathematics','0','1','0','absent','2025-10-12','1','MAT231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','Mathematics','0','1','0','absent','2025-10-12','1','MAT231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','Mathematics','0','1','0','absent','2025-10-12','1','MAT231'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-12','3','CSE208'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','absent','2025-10-12','3','CSE208'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-12','3','CSE208'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-12','4','CSE208'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','absent','2025-10-12','4','CSE208'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-12','4','CSE208'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','2','2','100','present','2025-10-12','5','CSE210'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','2','2','100','absent','2025-10-12','5','CSE210'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-12','5','CSE210'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','0','1','0','absent','2025-10-12','7','CSE232'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','1','1','100','present','2025-10-12','7','CSE232'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','1','0','absent','2025-10-12','7','CSE232'),('st_3','test_student','90:78:b2:ce:71:63','53','7','CSE','0','2','0','absent','2025-10-22','4','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','0','2','0','absent','2025-10-22','4','CSE208'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','CSE','0','2','0','absent','2025-10-22','4','CSE208'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','CSE','0','2','0','absent','2025-10-22','4','CSE208'),('st_3','test_student','90:78:b2:ce:71:63','53','7','Mathematics','0','1','0','present','2025-11-12','1','MAT231'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','Mathematics','0','1','0','present','2025-11-12','1','MAT231'),('std_1','Maher Faisal Rafin','08:1c:6e:7d:e6:a5','53','7','Mathematics','0','1','0','absent','2025-11-12','1','MAT231'),('std_2','Sabbir_Ahmed','f4:bb:c7:8e:46:28','53','7','Mathematics','0','1','0','present','2025-11-12','1','MAT231'),('std_4','Snithik','b4:ba:6a:84:4a:db','53','7','Mathematics','0','1','0','present','2025-11-12','1','MAT231'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208'),('st_69','Faiyaz Majumder','c8:90:8a:90:98:43','53','7','CSE','60','100','60','absent','2025-11-12','1','CSE208');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classroom`
--

DROP TABLE IF EXISTS `classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classroom` (
  `room_id` varchar(5) DEFAULT NULL,
  `period_no` varchar(2) DEFAULT NULL,
  `section` varchar(2) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `intake` varchar(5) DEFAULT NULL,
  `saturday` varchar(10) DEFAULT NULL,
  `sunday` varchar(10) DEFAULT NULL,
  `monday` varchar(10) DEFAULT NULL,
  `tuesday` varchar(10) DEFAULT NULL,
  `wednesday` varchar(10) DEFAULT NULL,
  `thursday` varchar(10) DEFAULT NULL,
  `friday` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classroom`
--

LOCK TABLES `classroom` WRITE;
/*!40000 ALTER TABLE `classroom` DISABLE KEYS */;
INSERT INTO `classroom` VALUES ('200','1','7','CSE','53','MAT231','MAT231','MAT231','MAT231','MAT231','MAT231','MAT231'),('200','2','7','CSE','53','CSE231','CSE209','CSE231','CSE209','CSE231','CSE209','CSE231'),('200','3','7','CSE','53','CSE209','CSE208','CSE209','CSE208','CSE209','CSE208','CSE209'),('200','4','7','CSE','53','CSE215','CSE208','MAT231','CSE215','CSE208','MAT231','CSE215'),('200','5','7','CSE','53','CSE207','CSE210','CSE207','CSE210','CSE207','CSE210','CSE207'),('200','6','7','CSE','53','CSE215','CSE210','CSE207','CSE215','CSE210','CSE207','CSE215'),('200','7','7','CSE','53','CSE231','CSE232','CSE231','CSE232','CSE231','CSE232','CSE231'),('200','8','7','CSE','53','CSE232','CSE232','CSE232','CSE232','CSE232','CSE232','CSE232');
/*!40000 ALTER TABLE `classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `client_id` varchar(20) NOT NULL,
  `setup` varchar(10) DEFAULT NULL,
  `token` varchar(20) DEFAULT NULL,
  `room_id` varchar(5) DEFAULT NULL,
  `subnet` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` varchar(10) NOT NULL,
  `course_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('CSE207','Database Management System Lab'),('CSE208','Database Management System'),('CSE209','Operating Systems'),('CSE210','Operating Systems Lab'),('CSE215','Architecture'),('CSE231','Algorithms'),('CSE232','Algorithms Lab'),('MAT231','Mathematics');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `period`
--

DROP TABLE IF EXISTS `period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `period` (
  `number` varchar(2) DEFAULT NULL,
  `start_time` varchar(10) DEFAULT NULL,
  `end_time` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `period`
--

LOCK TABLES `period` WRITE;
/*!40000 ALTER TABLE `period` DISABLE KEYS */;
INSERT INTO `period` VALUES ('1','8:00','10:59'),('2','11:00','13:59'),('3','14:00','16:59'),('4','17:00','19:59'),('5','20:00','22:59'),('6','23:00','1:59'),('7','2:00','4:59'),('8','5:00','7:59');
/*!40000 ALTER TABLE `period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `periods`
--

DROP TABLE IF EXISTS `periods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `periods` (
  `number` int DEFAULT NULL,
  `start_time` varchar(7) DEFAULT NULL,
  `end_time` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periods`
--

LOCK TABLES `periods` WRITE;
/*!40000 ALTER TABLE `periods` DISABLE KEYS */;
INSERT INTO `periods` VALUES (1,'8:00','9:59'),(2,'10:00','11:59'),(3,'12:00','13:59'),(4,'14:00','15:59'),(5,'16:00','17:59'),(6,'18:00','19:59'),(7,'20:00','21:59'),(8,'22:00','23:59');
/*!40000 ALTER TABLE `periods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` varchar(30) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mac` varchar(50) DEFAULT NULL,
  `intake` varchar(5) DEFAULT NULL,
  `section` varchar(10) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('st_3','test_student',NULL,'90:78:b2:ce:71:63','53','7','CSE','1234'),('st_6','someone','someone@gmail.com','11:22:33:44:55:66','53','7','Mathematics','1234'),('st_69','Faiyaz Majumder',NULL,'c8:90:8a:90:98:43','53','7','CSE','1234'),('std_1','Maher Faisal Rafin',NULL,'08:1c:6e:7d:e6:a5','53','7','CSE','1234'),('std_2','Sabbir_Ahmed',NULL,'f4:bb:c7:8e:46:28','53','7','CSE','1234'),('std_4','Snithik','test@gmail.com','b4:ba:6a:84:4a:db','53','7','CSE','2134'),('t_22','123456789123456789',NULL,'1234567891','54','34','123456789123456789','1234'),('t_24','123456789123456789',NULL,'11:22:33:44:55:66','12','12','CSE','1234');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `id` varchar(20) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `mac` varchar(50) DEFAULT NULL,
  `department` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('t_1','Khayrul Rahman','11:22:33:44:55:66','Mathematics','khayrul_rahman@gmail.com','1234'),('t_2','Ishita Nowshins','22:33:44:55:66:77','CSE','ishita_nowshin@gmail.com','12345'),('t_3','Farha Akter Munmun','1234','CSE','farhaaktermunmun@gmail.com','1234'),('t_4','safo','11:22:33:44:55:66','CSE','safo@gmail.com','1234'),('t_5','Sworna_Akter','11:22:33:44:55:66','CSE','sworna_akter@gmail.com','12345');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-12 21:25:23

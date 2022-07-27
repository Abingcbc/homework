/*
 Navicat Premium Data Transfer

 Source Server         : webcraft
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : webcraft

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 05/06/2020 23:46:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for GameFile
-- ----------------------------
DROP TABLE IF EXISTS `GameFile`;
CREATE TABLE `GameFile` (
  `fileId` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `updateTime` datetime DEFAULT NULL,
  `fileContent` text,
  `worldSize` int(11) DEFAULT NULL,
  PRIMARY KEY (`fileId`),
  KEY `GameFile_User_username_fk` (`username`),
  CONSTRAINT `GameFile_User_username_fk` FOREIGN KEY (`username`) REFERENCES `gameuser` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for GameUser
-- ----------------------------
DROP TABLE IF EXISTS `GameUser`;
CREATE TABLE `GameUser` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

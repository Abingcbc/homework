/*
 Navicat Premium Data Transfer

 Source Server         : tjmall
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : tjmall

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 28/05/2020 11:53:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for MallCart
-- ----------------------------
DROP TABLE IF EXISTS `MallCart`;
CREATE TABLE `MallCart` (
  `username` varchar(255) NOT NULL,
  `productId` int(11) NOT NULL,
  `number` int(11) DEFAULT NULL,
  KEY `cart_product_productId_fk` (`productId`),
  KEY `cart_user_username_fk` (`username`),
  CONSTRAINT `cart_product_productId_fk` FOREIGN KEY (`productId`) REFERENCES `mallproduct` (`productId`),
  CONSTRAINT `cart_user_username_fk` FOREIGN KEY (`username`) REFERENCES `malluser` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for MallOrder
-- ----------------------------
DROP TABLE IF EXISTS `MallOrder`;
CREATE TABLE `MallOrder` (
  `orderId` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `productId` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `createTime` datetime DEFAULT NULL,
  PRIMARY KEY (`orderId`),
  KEY `order_product_productId_fk` (`productId`),
  KEY `order_user_username_fk` (`username`),
  CONSTRAINT `order_product_productId_fk` FOREIGN KEY (`productId`) REFERENCES `mallproduct` (`productId`),
  CONSTRAINT `order_user_username_fk` FOREIGN KEY (`username`) REFERENCES `malluser` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of MallOrder
-- ----------------------------
BEGIN;
INSERT INTO `MallOrder` VALUES (1, '1', 1, 2, '2020-05-23 11:56:12');
INSERT INTO `MallOrder` VALUES (2, '1', 1, 1, '2020-05-23 15:10:32');
INSERT INTO `MallOrder` VALUES (3, '1', 1, 1, '2020-05-23 15:27:48');
INSERT INTO `MallOrder` VALUES (4, '1', 3, 1, '2020-05-23 23:05:11');
COMMIT;

-- ----------------------------
-- Table structure for MallProduct
-- ----------------------------
DROP TABLE IF EXISTS `MallProduct`;
CREATE TABLE `MallProduct` (
  `productId` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `originalPrice` decimal(11,2) DEFAULT NULL,
  `newPrice` decimal(11,2) DEFAULT NULL,
  `imageUrl` varchar(255) DEFAULT NULL,
  `detailUrls` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`productId`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of MallProduct
-- ----------------------------
BEGIN;
INSERT INTO `MallProduct` VALUES (1, '一次性三层口罩夏天薄款透气防尘', 99.00, 25.70, 'https://gju4.alicdn.com/bao/uploaded/i4/O1CN01oIvXc71VI7rB8dx4T_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i3/2201231852629/O1CN01iulHDS1VI7qUnaHhn_!!2201231852629.jpg_.webp|https://img.alicdn.com/imgextra/i2/2201231852629/O1CN01m46Mp01VI7rCnbrgT_!!2201231852629.jpg_.webp|https://img.alicdn.com/imgextra/i1/2201231852629/O1CN017S8BbC1VI7qTE0WUz_!!2201231852629.jpg_.webp|https://img.alicdn.com/imgextra/i4/2201231852629/O1CN01ttt9CJ1VI7qO65ZA4_!!2201231852629.jpg_.webp');
INSERT INTO `MallProduct` VALUES (2, '乐锦记奶香手撕棒早餐小面包', 39.60, 29.80, 'https://gju2.alicdn.com/bao/uploaded/i1/O1CN01gSRVC21XK4lOkScdB_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i4/2455082904/TB2Tul5iOOYBuNjSsD4XXbSkFXa_!!2455082904.jpg_.webp|https://img.alicdn.com/imgextra/i3/2455082904/TB24Rj4frZnBKNjSZFGXXbt3FXa_!!2455082904.jpg_.webp|https://img.alicdn.com/imgextra/i2/2455082904/TB2mZSOfCMmBKNjSZTEXXasKpXa_!!2455082904.jpg_.webp|https://img.alicdn.com/imgextra/i4/2455082904/TB2jwcffBsmBKNjSZFsXXaXSVXa_!!2455082904.jpg_.webp');
INSERT INTO `MallProduct` VALUES (3, '现货一次性三层防护口罩防尘防飞沫', 69.00, 7.90, 'https://gju4.alicdn.com/bao/uploaded/i3/2883691389/O1CN011u1AFX1M8CjWOnWSd_!!2883691389-0-lubanu-s.jpg_100x100Q90.jpg', 'https://img.alicdn.com/imgextra/i2/2883691389/O1CN01OvqB1E1M8CjbyieIr_!!2883691389.jpg_.webp|https://img.alicdn.com/imgextra/i3/2883691389/O1CN01etLDSI1M8CjcyBsDz_!!2883691389.jpg_.webp|https://img.alicdn.com/imgextra/i4/2883691389/O1CN01Oa8yCx1M8CjbO7ZQl_!!2883691389.jpg_.webp');
INSERT INTO `MallProduct` VALUES (4, '良品铺子岩焗乳酪吐司——进口新西兰安佳干酪', 45.00, 35.90, 'https://gju1.alicdn.com/bao/uploaded/i2/619123122/O1CN01SgIcmz1Yvv6SkdS61_!!619123122.jpg_100x100Q90.jpg', 'https://img.alicdn.com/imgextra/i4/619123122/O1CN01T17RxR1Yvv6vkTiIO_!!619123122.jpg_.webp|https://img.alicdn.com/imgextra/i3/619123122/O1CN01evNsTu1Yvv6vIiviO_!!619123122.jpg_.webp');
INSERT INTO `MallProduct` VALUES (5, '回头客卡侬尼华夫饼500g网红零食', 128.00, 38.80, 'https://gju4.alicdn.com/bao/uploaded/i4/O1CN01eip6Dx1pGYov9KXu0_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i2/2074475333/O1CN01xIazh61pGYosUVAB2_!!2074475333.jpg_.webp|https://img.alicdn.com/imgextra/i2/2074475333/O1CN01Tnvfhl1pGYotrtOGl_!!2074475333.jpg_.webp|https://img.alicdn.com/imgextra/i1/2074475333/O1CN01sTxMGR1pGYou9QV8r_!!2074475333.jpg_.webp|https://img.alicdn.com/imgextra/i2/2074475333/O1CN01kpb7941pGYotrm4MA_!!2074475333.jpg_.webp');
INSERT INTO `MallProduct` VALUES (6, '德佑75%度酒精消毒湿巾小包', 69.00, 39.90, 'https://gju4.alicdn.com/bao/uploaded/i4/O1CN01cXPL4H1a3zi6ypgbQ_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i2/2940753275/O1CN01THy0Y01a3zhZPwxtV_!!2940753275.jpg_.webp|https://img.alicdn.com/imgextra/i2/2940753275/O1CN01vMLYEb1a3zhj0xjxi_!!2940753275.jpg_.webp|https://img.alicdn.com/imgextra/i3/2940753275/O1CN01htfWY91a3zhnt3KQo_!!2940753275.jpg_.webp');
INSERT INTO `MallProduct` VALUES (7, '猴菇饼干整箱猴头菇饼干无糖精饼干', 48.00, 10.10, 'https://gju4.alicdn.com/bao/uploaded/i2/O1CN01GkMlvu1vbyy1fJLkq_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i2/3300766192/O1CN011kunCV1vbyvyQypoL_!!3300766192.jpg_.webp|https://img.alicdn.com/imgextra/i4/3300766192/O1CN01BET5cO1vbyvyQxtcS_!!3300766192.jpg_.webp|https://img.alicdn.com/imgextra/i3/3300766192/O1CN01Qg2y8Q1vbyvAH03DB_!!3300766192.jpg_.webp');
INSERT INTO `MallProduct` VALUES (8, '一次性3D立体口罩夏季轻薄透气防尘', 59.90, 13.20, 'https://gju3.alicdn.com/bao/uploaded/i3/O1CN018qlrC21VI7rCtO0XX_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i3/2201231852629/O1CN01iulHDS1VI7qUnaHhn_!!2201231852629.jpg_.webp|https://img.alicdn.com/imgextra/i2/2201231852629/O1CN01wjZvsh1VI7qlHDhgm_!!2201231852629.jpg_.webp|https://img.alicdn.com/imgextra/i2/2201231852629/O1CN01PV3UcA1VI7rETMUP2_!!2201231852629.jpg_.webp');
INSERT INTO `MallProduct` VALUES (9, '豪士早餐吐司乳酸菌口袋夹心全麦面', 59.90, 28.90, 'https://gju3.alicdn.com/bao/uploaded/i1/O1CN01Fg4Vqv1PwzOyEiHAZ_!!0-juitemmedia.jpg_560x560Q90.jpg', 'https://img.alicdn.com/imgextra/i2/2844431906/O1CN010CNGo21PwzUd5GMy2_!!2844431906.jpg_.webp|https://img.alicdn.com/imgextra/i3/2844431906/O1CN01pazd2g1PwzOt0KLPf_!!2844431906.jpg_.webp|https://img.alicdn.com/imgextra/i2/2844431906/O1CN01Pecvsl1PwzOstZMDQ_!!2844431906.jpg_.webp|https://img.alicdn.com/imgextra/i4/2844431906/O1CN01LU8ZCt1PwzOuzStKG_!!2844431906.jpg_.webphttps://img.alicdn.com/imgextra/i4/2844431906/O1CN01szYhMR1PwzOtfLXap_!!2844431906.jpg_.webp');
INSERT INTO `MallProduct` VALUES (10, '来伊份柔软原味蛋糕230g——32.5%鲜鸡蛋', 39.90, 22.90, 'https://gju2.alicdn.com/bao/uploaded/i3/732501769/O1CN01NjhGRj1OwFEvZNrYI_!!732501769.jpg_100x100Q90.jpg', 'https://img.alicdn.com/imgextra/i2/732501769/O1CN01VppPSx1OwFE3SrEDq_!!732501769.jpg_.webp|https://img.alicdn.com/imgextra/i1/732501769/O1CN01dCNTpl1OwFASGXShn_!!732501769.jpg_.webp|https://img.alicdn.com/imgextra/i1/732501769/O1CN01nm6h3i1OwFAS0l2p4_!!732501769.jpg_.webp|https://img.alicdn.com/imgextra/i2/732501769/O1CN012yIxRs1OwFASqdnY4_!!732501769.jpg_.webp');
COMMIT;

-- ----------------------------
-- Table structure for MallUser
-- ----------------------------
DROP TABLE IF EXISTS `MallUser`;
CREATE TABLE `MallUser` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of MallUser
-- ----------------------------
BEGIN;
INSERT INTO `MallUser` VALUES ('1', '1');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

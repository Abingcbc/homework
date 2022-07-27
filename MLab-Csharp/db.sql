CREATE TABLE `User` (
`username` varchar(255) NOT NULL,
`password` varchar(255) NOT NULL,
PRIMARY KEY (`username`) 
);
CREATE TABLE `Post` (
`postId` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(255) NULL,
`title` varchar(255) NULL,
`containerId` int(11) NULL,
`content` varchar(1023) NULL,
`createTime` datetime NULL,
`likeNum` int(11) NULL,
`commentNum` int(11) NULL,
`status` int(1) NULL,
PRIMARY KEY (`postId`) 
);
CREATE TABLE `Likes` (
`likeId` int(11) NOT NULL AUTO_INCREMENT,
`postId` int(11) NULL,
`username` varchar(255) NULL,
`status` int(1) NULL,
`createTime` datetime NULL,
PRIMARY KEY (`likeId`) 
);
CREATE TABLE `Comment` (
`commentId` int(11) NOT NULL AUTO_INCREMENT,
`postId` int(11) NULL,
`username` varchar(255) NULL,
`content` varchar(1023) NULL,
`createTime` datetime NULL,
`status` int(1) NULL,
PRIMARY KEY (`commentId`) 
);
CREATE TABLE `Container` (
`containerId` int(11) NOT NULL,
`username` varchar(255) NULL,
`createTime` datetime NULL,
`type` int NULL,
PRIMARY KEY (`containerId`) 
);

ALTER TABLE `Post` ADD CONSTRAINT `fk_POST` FOREIGN KEY (`username`) REFERENCES `User` (`username`);
ALTER TABLE `Likes` ADD CONSTRAINT `fk_LIKE` FOREIGN KEY (`username`) REFERENCES `User` (`username`);
ALTER TABLE `Likes` ADD CONSTRAINT `fk_LIKE_1` FOREIGN KEY (`postId`) REFERENCES `Post` (`postId`);
ALTER TABLE `Comment` ADD CONSTRAINT `fk_COMMENT` FOREIGN KEY (`postId`) REFERENCES `Post` (`postId`);
ALTER TABLE `Comment` ADD CONSTRAINT `fk_COMMENT_1` FOREIGN KEY (`username`) REFERENCES `User` (`username`);
ALTER TABLE `Post` ADD CONSTRAINT `fk_POST_1` FOREIGN KEY (`containerId`) REFERENCES `Container` (`containerId`);
ALTER TABLE `Container` ADD CONSTRAINT `fk_Container` FOREIGN KEY (`username`) REFERENCES `User` (`username`);


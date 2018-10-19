请将下面的SQL语句执行，然后默认登录账号是54php.cn 密码是123456

INSERT INTO `user` (`uid`, `nickname`, `mobile`, `email`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`)
VALUES
	(1, '编程浪子www.54php.cn', '11012345679', 'apanly@163.com', 1, '', '54php.cn', '816440c40b7a9d55ff9eb7b20760862c', 'cF3JfH5FJfQ8B2Ba', 1, '2017-03-15 14:08:48', '2017-03-15 14:08:48');


INSERT INTO `platform` (`name`, `province`, `city`, `description`,`status`)
VALUES
	('淘鲜蜂', '江苏省', '太仓市',  '太仓淘鲜蜂',1);

INSERT INTO `platform` (`name`, `province`, `city`, `description`,`status`)
VALUES
	('博奥优选', '江苏省', '南通市',  '南通博奥优选',1);


INSERT INTO `community` (`platform_id`, `platform_name`, `name`, `province`, `city`, `description`, `pickups`,`status`) 
	VALUES ('1', '淘鲜蜂', '华侨花园', '江苏省', '太仓市', '太仓华侨花园', '华侨A,华侨B',1);

INSERT INTO `community` (`platform_id`, `platform_name`, `name`, `province`, `city`, `description`, `pickups`,`status`) 
	VALUES ('1', '淘鲜蜂', '洋沙5组', '江苏省', '太仓市', '太仓华侨花园', '洋沙A',1);

INSERT INTO `community` (`platform_id`, `platform_name`, `name`, `province`, `city`, `description`, `pickups`,`status`) 
	VALUES ('2', '博奥优选', '皇家花苑', '江苏省', '南通市', '南通皇家花苑', '皇家A',1);


INSERT INTO `user` (`uid`,`platform_id`,`community_id`,`platform_name`,`community_name`, `nickname`, `mobile`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`)
VALUES
	(1,1,null,'淘鲜蜂',null, '淘鲜蜂admin', '11012345679', 1, '', '淘鲜蜂admin', '816440c40b7a9d55ff9eb7b20760862c', 'cF3JfH5FJfQ8B2Ba', 1, '2017-03-15 14:08:48', '2017-03-15 14:08:48');

INSERT INTO `user` (`uid`,`platform_id`,`community_id`,`platform_name`,`community_name`, `nickname`, `mobile`, `email`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`)
VALUES
	(2,1,1,'淘鲜蜂','华侨花园', '华侨花园', '11012345679', 'apanly@163.com', 1, '', '华侨花园', '816440c40b7a9d55ff9eb7b20760862c', 'cF3JfH5FJfQ8B2Ba', 1, '2017-03-15 14:08:48', '2017-03-15 14:08:48');	

INSERT INTO `user` (`uid`,`platform_id`,`community_id`,`platform_name`,`community_name`, `nickname`, `mobile`, `email`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`)
VALUES
	(3,1,1,'淘鲜蜂','洋沙5村', '洋沙5村', '11012345679', 'apanly@163.com', 1, '', '洋沙5村', '816440c40b7a9d55ff9eb7b20760862c', 'cF3JfH5FJfQ8B2Ba', 1, '2017-03-15 14:08:48', '2017-03-15 14:08:48');	


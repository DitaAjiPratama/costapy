-- README
-- idx_ = index
-- fk_  = foreign
-- Create an index for fast lookups
-- Defining constraints separately for better readability & maintainability
-- NOTE
-- Next verification variation should be based from identity and contact

CREATE TABLE `auth` (
	`token` 		binary(40) 		NOT NULL PRIMARY KEY,
	`password` 		binary(60) 		NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_roles` (
	`id` 			int(11) 		NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` 			varchar(36) 	NOT NULL UNIQUE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_session` (
	`id` 			int(11) 		NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`token` 		binary(40)		NOT NULL,
	`start` 		datetime 		NOT NULL,
	`end` 			datetime 		DEFAULT NULL,
	KEY 			`idx_token` 	(`token`), 
	CONSTRAINT `auth_session_fk_token`
		FOREIGN KEY (`token`) REFERENCES `auth` (`token`)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_profile` (
	`id` 			int(11) 		NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`token` 		binary(40) 		NOT NULL,
	`username` 		varchar(36) 	NOT NULL UNIQUE,
	`email` 		longtext 		DEFAULT NULL,
	`phone` 		bigint(20) 		DEFAULT NULL,
	KEY 			`idx_token` 	(`token`),
	CONSTRAINT `auth_profile_fk_token`
		FOREIGN KEY (`token`) REFERENCES `auth` (`token`)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_profile_verification` (
	`id` 			int(11) 		NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`profile` 		int(11) 		NOT NULL,
	`type` 			longtext 		DEFAULT NULL, -- Can be email, ID card, phone, etc
	`verified` 		int(1) 			DEFAULT 0,
	KEY 			`idx_profile` 	(`profile`),
	CONSTRAINT `auth_profile_verification_fk_profile`
		FOREIGN KEY (`profile`) REFERENCES `auth_profile` (`id`)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_profile_roles` (
	`id` 			int(11) 		NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`profile` 		int(11) 		NOT NULL,
	`roles` 		int(11) 		NOT NULL,
	KEY 			`idx_profile` 	(`profile`),
	KEY 			`idx_roles` 	(`roles`),
	CONSTRAINT `auth_profile_roles_fk_profile`
		FOREIGN KEY (`profile`) REFERENCES `auth_profile` (`id`)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT `auth_profile_roles_fk_roles`
		FOREIGN KEY (`roles`) REFERENCES `auth_roles` (`id`)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

INSERT INTO `auth_roles` VALUES
(1, 'su'		),
(2, 'admin'		),
(3, 'member'	),
(4, 'tester'	);


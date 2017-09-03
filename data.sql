CREATE TABLE url (
	`id` 			INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`last_scrap` 	DATETIME,
	`last_success`	DATETIME,
	`success`		INTEGER DEFAULT 0,
	`url_dir`		VARCHAR(500)
);

CREATE TABLE grade (
	`id`		INTEGER PRIMARY KEY AUTO_INCREMENT,
	`type`		VARCHAR(500),
	`active`	INTEGER
);

CREATE TABLE price (
	`id`			INTEGER PRIMARY KEY AUTO_INCREMENT,
	`grade`			INTEGER NULL,
	`sell_price`	FLOAT,
	`buy_price`		FLOAT,
	`voucher_price`	FLOAT,
	FOREIGN KEY(`grade`) REFERENCES `grade`(`id`)
);

CREATE TABLE category (
	`id`			INTEGER PRIMARY KEY AUTO_INCREMENT,
	`name`			VARCHAR(500) UNIQUE
);

CREATE TABLE subcategory (
	`id`		INTEGER PRIMARY KEY AUTO_INCREMENT,
	`name`		VARCHAR(500) UNIQUE,
	`category`	INTEGER NULL,
	FOREIGN KEY(`category`) REFERENCES `category`(`id`)
);

CREATE TABLE product (
	`id`				INTEGER PRIMARY KEY AUTO_INCREMENT,
	`make`				VARCHAR(500),
	`model`				VARCHAR(500),
	`colour`			VARCHAR(500),
	`capacity`			VARCHAR(500),
	`img`				VARCHAR(500),
	`sku`				VARCHAR(500),
	`url`				INTEGER NOT NULL,
	`category`			INTEGER NOT NULL,
	`sub_category`		INTEGER NOT NULL,
	`grade`				INTEGER NULL,
	`price`				INTEGER NOT NULL,
	`last_updated`		DATETIME,
	`frequent`			INTEGER DEFAULT 0,
	`name`				VARCHAR(500),
	FOREIGN KEY(`url`) REFERENCES `url`(`id`),
	FOREIGN KEY(`grade`) REFERENCES `grade`(`id`),
	FOREIGN KEY(`sub_category`) REFERENCES `category`(`id`),
	FOREIGN KEY(`category`) REFERENCES `category`(`id`),
	FOREIGN KEY(`price`) REFERENCES `price`(`id`)
);
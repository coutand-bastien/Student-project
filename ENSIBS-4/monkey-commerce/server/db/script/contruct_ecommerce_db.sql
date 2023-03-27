CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

--
-- Table structure for table customer
--
CREATE TABLE IF NOT EXISTS customer (
    id int not null auto_increment,
    name varchar(45) not null,
    email varchar(45) not null,
    phone varchar(45) not null,
    address varchar(45) not null,
    city_region varchar(2) not null,
    cc_number varchar(19) not null,

    CONSTRAINT PK_customer PRIMARY KEY (id)
) ENGINE=InnoDB auto_increment=1 DEFAULT CHARSET=latin1;


--
-- Table structure for table customer_order
--
CREATE TABLE IF NOT EXISTS customer_order (
    id int not null auto_increment,
    amount decimal(6,2) not null ,
    date_created timestamp default current_timestamp not null,
    confirmation_number int not null,
    customer_id int not null,

    CONSTRAINT PK_category PRIMARY KEY (id),
    CONSTRAINT FK_customer_order_customer FOREIGN KEY (customer_id) REFERENCES customer(id)
) ENGINE=InnoDB auto_increment=1 DEFAULT CHARSET=latin1;


--
-- Table structure for table category
--
CREATE TABLE IF NOT EXISTS category (
    id tinyint not null auto_increment,
    name varchar(45) not null,
    description varchar(255) not null,

    CONSTRAINT PK_category PRIMARY KEY (id)
) ENGINE=InnoDB auto_increment=1 DEFAULT CHARSET=latin1;


--
-- Table structure for table product
--
CREATE TABLE IF NOT EXISTS product (
    id int not null auto_increment,
    name varchar(45) not null,
    price decimal(5,2) not null,
    description tinytext not null,
    last_update timestamp default current_timestamp on update current_timestamp not null,
    base_quantity int not null,
    category_id tinyint not null,

    CONSTRAINT PK_product PRIMARY KEY (id),
    CONSTRAINT FK_product_category FOREIGN KEY (category_id) REFERENCES category(id)
) ENGINE=InnoDB auto_increment=1 DEFAULT CHARSET=latin1;

--
-- Table structure for table customer_order_has_product
--
CREATE TABLE IF NOT EXISTS ordered_product (
    customer_order_id int not null,
    product_id int not null,

    CONSTRAINT PK_customer_order PRIMARY KEY (customer_order_id, product_id),
    CONSTRAINT FK_customer_order_product FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT FK_customer_order_customer_order FOREIGN KEY (customer_order_id) REFERENCES customer_order(id)
) ENGINE=InnoDB auto_increment=1 DEFAULT CHARSET=latin1;


--
-- Data for table customer
--
INSERT INTO customer VALUES (1, 'John Doe', 'john.doe@gmail.com', '123-456-7890', '123 Main St', 'NY', '1234-5678-9012-3456');
INSERT INTO customer VALUES (2, 'Jane Doe', 'jane.doe@outlook.com', '098-765-4321', '456 Main St', 'NY', '1234-5678-9012-3456');

--
-- Data for table customer_order
--
INSERT INTO customer_order VALUES (1, 100.00, '2018-01-01 00:00:00', 123456, 1);
INSERT INTO customer_order VALUES (2, 200.00, '2018-01-01 00:00:00', 123456, 2);

--
-- Data for table categorie
--
INSERT INTO category VALUES (1, 'Electronics', 'Electronics category');
INSERT INTO category VALUES (2, 'Furniture', 'Furniture category');
INSERT INTO category VALUES (3, 'Clothes', 'Clothes category');
INSERT INTO category VALUES (4, 'Books', 'Books category');
INSERT INTO category VALUES (5, 'Music', 'Music category');
INSERT INTO category VALUES (6, 'Movies', 'Movies category');
INSERT INTO category VALUES (7, 'Games', 'Games category');
INSERT INTO category VALUES (8, 'Toys', 'Toys category');

--
-- Data for table product
--
INSERT INTO product VALUES (1, 'iPhone', 100.00, 'iPhone 7', '2018-01-01 00:00:00', 12, 1);
INSERT INTO product VALUES (2, 'iPad', 500.00, 'iPad Pro', '2018-01-01 00:00:00', 8, 1);
INSERT INTO product VALUES (3, 'MacBook', 200.00, 'MacBook Pro', '2018-01-01 00:00:00', 5, 1);

INSERT INTO product VALUES (4, 'Chair', 100.00, 'Office Chair', '2018-01-01 00:00:00', 12, 2);
INSERT INTO product VALUES (5, 'Table', 200.00, 'Office Table', '2018-01-01 00:00:00', 1, 2);
INSERT INTO product VALUES (6, 'Desk', 300.00, 'Office Desk', '2018-01-01 00:00:00', 8, 2);

INSERT INTO product VALUES (7, 'Shirt', 50.00, 'T-Shirt', '2018-01-01 00:00:00', 12, 3);
INSERT INTO product VALUES (8, 'Pants', 100.00, 'Jeans', '2018-01-01 00:00:00', 8, 3);
INSERT INTO product VALUES (9, 'Shoes', 200.00, 'Sneakers', '2018-01-01 00:00:00', 5, 3);

INSERT INTO product VALUES (10, 'Harry Potter', 20.00, 'Harry Potter and the Sorcerer\'s Stone', '2018-01-01 00:00:00', 12, 4);
INSERT INTO product VALUES (11, 'Lord of the Rings', 30.00, 'The Fellowship of the Ring', '2018-01-01 00:00:00', 8, 4);
INSERT INTO product VALUES (12, 'Game of Thrones', 40.00, 'A Game of Thrones', '2018-01-01 00:00:00', 5, 4);

INSERT INTO product VALUES (13, 'The Beatles', 20.00, 'Abbey Road', '2018-01-01 00:00:00', 12, 5);
INSERT INTO product VALUES (14, 'Michael Jackson', 30.00, 'Thriller', '2018-01-01 00:00:00', 8, 5);
INSERT INTO product VALUES (15, 'Elvis Presley', 40.00, 'Elvis Presley', '2018-01-01 00:00:00', 5, 5);

INSERT INTO product VALUES (16, 'Star Wars', 20.00, 'Star Wars: Episode IV - A New Hope', '2018-01-01 00:00:00', 12, 6);
INSERT INTO product VALUES (17, 'The Godfather', 30.00, 'The Godfather', '2018-01-01 00:00:00', 8, 6);
INSERT INTO product VALUES (18, 'The Shawshank Redemption', 40.00, 'The Shawshank Redemption', '2018-01-01 00:00:00', 5, 6);

INSERT INTO product VALUES (19, 'Call of Duty', 20.00, 'Call of Duty: Black Ops', '2018-01-01 00:00:00', 12, 7);
INSERT INTO product VALUES (20, 'Minecraft', 30.00, 'Minecraft', '2018-01-01 00:00:00', 8, 7);
INSERT INTO product VALUES (21, 'Fortnite', 40.00, 'Fortnite', '2018-01-01 00:00:00', 5, 7);

INSERT INTO product VALUES (22, 'Lego', 20.00, 'Lego Star Wars', '2018-01-01 00:00:00', 12, 8);
INSERT INTO product VALUES (23, 'Barbie', 30.00, 'Barbie Doll', '2018-01-01 00:00:00', 8, 8);
INSERT INTO product VALUES (24, 'Hot Wheels', 40.00, 'Hot Wheels Car', '2018-01-01 00:00:00', 5, 8);


--
-- Data for table customer_order_has_product
--
INSERT INTO ordered_product VALUES (1, 1);
INSERT INTO ordered_product VALUES (1, 2);
INSERT INTO ordered_product VALUES (1, 3);
INSERT INTO ordered_product VALUES (2, 4);
INSERT INTO ordered_product VALUES (2, 5);
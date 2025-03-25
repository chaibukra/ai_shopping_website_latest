DROP TABLE IF EXISTS user_favorite_item;
DROP TABLE IF EXISTS item_order;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL
);

CREATE TABLE item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    image VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    shipping_address VARCHAR(255),
    order_status VARCHAR(100) NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE item_order (
    id INT AUTO_INCREMENT,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    item_quantity INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE user_favorite_item (
    id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)

);


INSERT INTO item (item_name, price, quantity,image)
 VALUES
    ('Laptop', 1200.00, 80,'ui/assets/images/Laptop.jpg'),
    ('Smartphone', 800.00, 60,'ui/assets/images/Smartphone.jpg'),
    ('Headphones', 200.00, 70,'ui/assets/images/Headphones.jpg'),
    ('Smartwatch', 300.00, 100,'ui/assets/images/Smartwatch.jpg'),
    ('Tablet', 500.00, 30,'ui/assets/images/Tablet.jpg'),
    ('Desktop PC', 850.00, 300,'ui/assets/images/Desktop PC.jpg'),
    ('Monitor', 350.00, 120,'ui/assets/images/Monitor.jpg'),
    ('Keyboard', 50.00, 300,'ui/assets/images/Keyboard.jpg'),
    ('Mouse', 25.00, 300,'ui/assets/images/Mouse.jpg'),
    ('Router', 150.00, 50,'ui/assets/images/Router.jpg');
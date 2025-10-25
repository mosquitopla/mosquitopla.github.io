import sqlite3
from datetime import date

conn = sqlite3.connect("processors.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Processors;
DROP TABLE IF EXISTS Brands;
DROP TABLE IF EXISTS Sockets;


CREATE TABLE Brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    contact_info TEXT
);


CREATE TABLE Sockets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    manufacturer TEXT
);


CREATE TABLE Processors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER,
    series TEXT,
    generation TEXT,
    cores INTEGER,
    threads INTEGER,
    base_clock REAL,
    boost_clock REAL,
    tdp INTEGER,
    socket_id INTEGER,
    release_year INTEGER,
    price_usd REAL,
    stock_quantity INTEGER,
    FOREIGN KEY (brand_id) REFERENCES Brands(id),
    FOREIGN KEY (socket_id) REFERENCES Sockets(id)
);


CREATE TABLE Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT
);


CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_price REAL,
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);


CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    processor_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (processor_id) REFERENCES Processors(id)
);
""")

brands = [
    ("Intel", "USA", "intel@example.com"),
    ("AMD", "USA", "amd@example.com")
    ("Apple", "USA", "Apple"),
    ("Qualcomm", "USA", "Qualcomm")
    
]
cursor.executemany("INSERT INTO Brands (name, country, contact_info) VALUES (?, ?, ?)", brands)

sockets = [
    ("LGA1200", "Socket for Intel 10th/11th Gen", "Intel"),
    ("AM4", "Socket for AMD Ryzen 1000-5000", "AMD")
    ("Apple M Socket", "Socket for Apple", "Apple"),
    ("Snapdragon SoC", "Socket for Snapdragon", "Snapdragon")
]
cursor.executemany("INSERT INTO Sockets (name, description, manufacturer) VALUES (?, ?, ?)", sockets)

processors = [
    ('Intel Core i5-13400F', 1, 'Core i5', '13th Gen', 10, 16, 2.5, 4.6, 65, 1, 2023, 210.00, 45),
    ('AMD Ryzen 7 7700X', 2, 'Ryzen 7', 'Zen 4', 8, 16, 4.5, 5.4, 105, 2, 2022, 349.00, 30),
    ('Apple M2 Pro', 3, 'M Series', 'M2 Gen', 10, 10, 3.2, 3.5, 30, 3, 2023, 599.00, 20),
    ('Qualcomm Snapdragon X Elite', 4, 'Snapdragon', 'X Elite', 12, 12, 3.8, 4.3, 45, 4, 2024, 499.00, 25),
    ('Intel Core i9-13900K', 1, 'Core i9', '13th Gen', 24, 32, 3.0, 5.8, 125, 1, 2023, 589.00, 18),
    ('AMD Ryzen 5 7600', 2, 'Ryzen 5', 'Zen 4', 6, 12, 3.8, 5.1, 65, 2, 2022, 229.00, 40),
    ('Apple M1', 3, 'M Series', 'M1 Gen', 8, 8, 3.2, 3.2, 20, 3, 2020, 399.00, 35),
    ('Qualcomm Snapdragon 8cx Gen 3', 4, 'Snapdragon', '8cx Gen 3', 8, 8, 3.0, 3.4, 15, 4, 2022, 299.00, 50),
    ('Intel Pentium Gold G7400', 1, 'Pentium Gold', 'Alder Lake', 2, 4, 3.7, 3.7, 46, 1, 2022, 89.00, 60),
    ('AMD Ryzen Threadripper PRO 5995WX', 2, 'Threadripper PRO', 'Zen 3', 64, 128, 2.7, 4.5, 280, 2, 2022, 6499.00, 5)
]

cursor.executemany("""
INSERT INTO Processors (name, brand_id, series, generation, cores, threads,
base_clock, boost_clock, tdp, socket_id, release_year, price_usd, stock_quantity)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", processors)

customers = [
    ("Олександр Іванов", "alex@example.com", "+380501234567", "Київ, вул. Хрещатик, 10"),
    ("Марія Петренко", "maria@example.com", "+380631112233", "Львів, вул. Дорошенка, 5")
]
cursor.executemany("INSERT INTO Customers (name, email, phone, address) VALUES (?, ?, ?, ?)", customers)

orders = [
    (1, str(date.today()), "new", 0),
    (2, str(date.today()), "new", 0)
]
cursor.executemany("INSERT INTO Orders (customer_id, order_date, status, total_price) VALUES (?, ?, ?, ?)", orders)

orders = [
    (1, str(date.today()), "new", 0),
    (2, str(date.today()), "new", 0)
]
cursor.executemany("INSERT INTO Orders (customer_id, order_date, status, total_price) VALUES (?, ?, ?, ?)", orders)

order_items = [
    (1, 1, 2, 180, 360),
    (1, 3, 1, 200, 200),
    (2, 2, 1, 350, 350)
]
cursor.executemany("INSERT INTO OrderItems (order_id, processor_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)", order_items)

cursor.execute("UPDATE Orders SET total_price = (SELECT SUM(subtotal) FROM OrderItems WHERE order_id = 1) WHERE id = 1")
cursor.execute("UPDATE Orders SET total_price = (SELECT SUM(subtotal) FROM OrderItems WHERE order_id = 2) WHERE id = 2")

conn.commit()
conn.close()


print("База даних створена і заповнена тестовими даними.")

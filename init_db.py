import sqlite3

DATABASE = "database.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    cover_image TEXT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    revenue REAL NOT NULL
)
""")

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM sales")

cursor.execute("""
INSERT INTO users (email, password, role)
VALUES (?, ?, ?)
""", ("admin@bookstore.com", "admin123", "admin"))

cursor.execute("""
INSERT INTO users (email, password, role)
VALUES (?, ?, ?)
""", ("user@bookstore.com", "user123", "user"))

books = [
    (
        "My Name is Red",
        "Orhan Pamuk",
        210.00,
        12,
        "red.jpg",
        "A historical novel set in the Ottoman Empire."
    ),
    (
        "The White Castle",
        "Orhan Pamuk",
        195.50,
        8,
        "white_castle.jpg",
        "A novel about identity, knowledge, and cultural exchange."
    ),
    (
        "The Time Regulation Institute",
        "Ahmet Hamdi Tanpınar",
        185.00,
        10,
        "time_institute.jpg",
        "A satirical novel about modernization and bureaucracy."
    )
]

cursor.executemany("""
INSERT INTO books (title, author, price, stock, cover_image, description)
VALUES (?, ?, ?, ?, ?, ?)
""", books)

sales = [
    ("Jan", 12000),
    ("Feb", 18000),
    ("Mar", 26000),
    ("Apr", 41000),
    ("May", 55000),
    ("Jun", 48000),
    ("Jul", 62000),
    ("Aug", 73000),
    ("Sep", 45000),
    ("Oct", 98000),
    ("Nov", 67000),
    ("Dec", 76000)
]

cursor.executemany("""
INSERT INTO sales (month, revenue)
VALUES (?, ?)
""", sales)

conn.commit()
conn.close()

print("Database initialized with users, books, and sales data.")
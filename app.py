from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "bookstore_secret_key"

DATABASE = "database.db"

def get_cart():
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def seed_golden_state(conn):
    conn.execute("DELETE FROM books")
    conn.execute("DELETE FROM sales")

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
        ),
        (
            "Crime and Punishment",
            "Fyodor Dostoevsky",
            160.00,
            15,
            "crime_punishment.jpg",
            "A psychological novel about guilt, morality, and redemption."
        ),
        (
            "1984",
            "George Orwell",
            145.00,
            20,
            "1984.jpg",
            "A dystopian novel about surveillance and authoritarianism."
        )
    ]

    conn.executemany("""
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

    conn.executemany("""
        INSERT INTO sales (month, revenue)
        VALUES (?, ?)
    """, sales)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("books"))

        error = "Invalid email or password."

    return render_template("login.html", error=error)


@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    sales = conn.execute("SELECT * FROM sales").fetchall()
    conn.close()

    months = [sale["month"] for sale in sales]
    revenues = [sale["revenue"] for sale in sales]

    return render_template(
        "admin.html",
        books=books,
        months=months,
        revenues=revenues
    )

@app.route("/admin/add-book", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    title = request.form["title"]
    author = request.form["author"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    cover_image = request.form["cover_image"]
    description = request.form["description"]

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO books (title, author, price, stock, cover_image, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, author, price, stock, cover_image, description))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-book/<int:book_id>")
def delete_book(book_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/generate-junk")
def generate_junk_data():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    junk_books = [
        ("book 1", "me", 0.00, -10, "missing.jpg", "bad data"),
        ("asdasdf", "test author", 9999999.00, 999, "", "random broken record"),
        ("test_book_final", "qwerty", 1.00, -5, "none", "temporary test item"),
        ("11111", "no author", 0.00, 0, "broken-image.png", ""),
        ("NULL_BOOK", "unknown", -100.00, -20, "", "corrupted price and stock")
    ]

    junk_sales = [
        ("Jan", -5000),
        ("Feb", 999999),
        ("Mar", 0),
        ("Apr", -12000),
        ("May", 850000),
        ("Jun", 5),
        ("Jul", 99999),
        ("Aug", -3000),
        ("Sep", 1),
        ("Oct", 700000),
        ("Nov", -100),
        ("Dec", 999999)
    ]

    conn = get_db_connection()

    conn.executemany("""
        INSERT INTO books (title, author, price, stock, cover_image, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, junk_books)

    conn.execute("DELETE FROM sales")

    conn.executemany("""
        INSERT INTO sales (month, revenue)
        VALUES (?, ?)
    """, junk_sales)

    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/reset-golden-state")
def reset_golden_state():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    seed_golden_state(conn)
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/add-to-cart/<int:book_id>")
def add_to_cart(book_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    cart = get_cart()
    cart.append(book_id)
    session["cart"] = cart

    return redirect(url_for("books"))


@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template("books.html", books=books)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cart_ids = get_cart()

    conn = get_db_connection()

    books = []
    total = 0

    for book_id in cart_ids:
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()

        if book:
            books.append(book)
            total += book["price"]

    conn.close()

    return render_template("cart.html", books=books, total=total)

@app.route("/checkout")
def checkout():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cart_ids = get_cart()

    conn = get_db_connection()

    total = 0
    for book_id in cart_ids:
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()

        if book:
            total += book["price"]

    # demo: satış verisine ekle (Dec ayına)
    conn.execute("""
        UPDATE sales
        SET revenue = revenue + ?
        WHERE month = 'Dec'
    """, (total,))

    conn.commit()
    conn.close()

    session["cart"] = []

    return redirect(url_for("books"))


if __name__ == "__main__":
    app.run(debug=True)
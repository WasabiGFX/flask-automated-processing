from flask import Flask, render_template, request, redirect, session
import sqlite3
# ADMIN LOGIN: email: admin@greenfield.com pass: 1111

#rename to app.py
app = Flask(__name__)
app.secret_key = "anothersecretkey"


# Connect to database
def connect_db():
    return sqlite3.connect("database.db")


# Setup database
def setup_database():
    db = connect_db()

    # Create tables
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER,
        producer TEXT,
        allergens TEXT,
        image_url TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        total REAL
    )
    """)

    db.commit()

    insert_test_data(db)


# Insert test data (separate function)
def insert_test_data(db):
    if db.execute("SELECT * FROM users").fetchone() is None:
        db.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            ("admin@greenfield.com", "1111", "admin")
        )

    if db.execute("SELECT * FROM products").fetchone() is None:
        products = [
            ("Apples", 2.5, 50, "Greenfield Farms", "None", "https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&w=500&q=60"),
            ("Milk", 1.2, 30, "Happy Cow Dairy", "Dairy", "https://images.immediate.co.uk/production/volatile/sites/30/2020/02/Glass-and-bottle-of-milk-fe0997a.jpg"),
            ("Bread", 1.0, 20, "Local Bakery", "Gluten, Wheat", "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=500&q=60")
        ]

        for product in products:
            db.execute(
                "INSERT INTO products (name, price, stock, producer, allergens, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                product
            )

    db.commit()


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def sign_in():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = connect_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user"] = user[0]
            session["role"] = user[3]
            return redirect("/")
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password != confirm_password:
            error = "Passwords do not match"
        else:
            db = connect_db()
            # Check if user already exists
            existing_user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if existing_user:
                error = "User already exists"
            else:
                db.execute(
                    "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                    (email, password, "user")
                )
                db.commit()
                return redirect("/login")

    return render_template("register.html", error=error)


# Logout
@app.route("/logout")
def sign_out():
    session.clear()
    return redirect("/")


# Admin Dashboard
@app.route("/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")
    
    db = connect_db()
    products = db.execute("SELECT * FROM products").fetchall()
    orders = db.execute("SELECT orders.id, products.name, orders.quantity, orders.total FROM orders JOIN products ON orders.product_id = products.id").fetchall()
    
    return render_template("dashboard.html", 
                           products=products, 
                           orders=orders)


# Dashboard Add Product
@app.route("/dashboard/add", methods=["POST"])
def dashboard_add():
    if session.get("role") != "admin":
        return redirect("/")
    
    name = request.form["name"]
    price = request.form["price"]
    stock = request.form["stock"]
    producer = request.form["producer"]
    allergens = request.form.get("allergens", "None")
    image_url = request.form.get("image_url", "https:")
    
    db = connect_db()
    db.execute(
        "INSERT INTO products (name, price, stock, producer, allergens, image_url) VALUES (?, ?, ?, ?, ?, ?)",
        (name, price, stock, producer, allergens, image_url)
    )
    db.commit()
    return redirect("/dashboard")


# Dashboard Update Product
@app.route("/dashboard/update/<int:product_id>", methods=["POST"])
def dashboard_update(product_id):
    if session.get("role") != "admin":
        return redirect("/")
    
    stock = request.form["stock"]
    
    db = connect_db()
    db.execute("UPDATE products SET stock=? WHERE id=?", (stock, product_id))
    db.commit()
    return redirect("/dashboard")


# Dashboard Delete Product
@app.route("/dashboard/delete/<int:product_id>", methods=["POST"])
def dashboard_delete(product_id):
    if session.get("role") != "admin":
        return redirect("/")
    
    db = connect_db()
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    return redirect("/dashboard")


# Catalogue
@app.route("/products")
def show_products():
    db = connect_db()
    items = db.execute("SELECT * FROM products").fetchall()
    return render_template("catalogue.html", products=items)


# Product page
@app.route("/product/<int:product_id>")
def view_product(product_id):
    db = connect_db()
    item = db.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    return render_template("product.html", product=item)


# Search
@app.route("/search")
def search_items():
    keyword = request.args.get("q")

    db = connect_db()
    results = db.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        ("%" + keyword + "%",)
    ).fetchall()

    return render_template("catalogue.html", products=results)


# Order
@app.route("/order", methods=["POST"])
def create_order():
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    db = connect_db()

    product = db.execute(
        "SELECT stock, price FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    if product:
        stock, price = product

        if quantity > 0 and stock >= quantity:
            total = price * quantity

            db.execute(
                "INSERT INTO orders (product_id, quantity, total) VALUES (?, ?, ?)",
                (product_id, quantity, total)
            )

            db.execute(
                "UPDATE products SET stock = stock - ? WHERE id=?",
                (quantity, product_id)
            )

            db.commit()

            return "Order complete"
        else:
            return "Error: invalid quantity or insufficient stock"

    return "Error: product not found"


# Run app
if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
import sqlite3

db = "myprotein.db"

def opendb():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return conn, c

def create_table():
    conn, c = opendb()
    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            image TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert(products):
    conn, c = opendb()

    for p in products:
        c.execute("""
            INSERT INTO products (title, price, image)
            VALUES (?, ?, ?)
        """, (p["title"], p["price"], p["image"]))

    conn.commit()
    conn.close()

def get_all_products():
    conn, c = opendb()
    c.execute("SELECT id, title, price, image FROM products")
    rows = c.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "title": r[1],
            "price": r[2],
            "image": r[3]
        })
    return result

def get_products_price(price_limit):
    """
    Tagastab tooted, mille hind on suurem.
    """
    conn, c = opendb()
    c.execute("""
        SELECT id, title, price, image
        FROM products
        WHERE price > ?
    """, (price_limit,))

    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "image": row[3]
        })
    return result

if __name__ == "__main__":
    create_table()
    print("DB created")

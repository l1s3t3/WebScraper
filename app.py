from flask import Flask, render_template, request
from db import get_all_products, get_products_price

app = Flask(__name__)

@app.route("/")
def index():
    products = get_all_products()
    return render_template("index.html", products=products)

@app.route("/filter", methods=["GET", "POST"])
def filter_products():
    if request.method == "POST":
        price = request.form.get("price_limit").replace(",", ".")
        try:
            price_limit = float(price)
        except:
            price_limit = 0.0

        filtered = get_products_price(price_limit)
        return render_template("result.html", products=filtered, limit=price_limit)
    return render_template("filter.html")

if __name__ == "__main__":
    app.run()

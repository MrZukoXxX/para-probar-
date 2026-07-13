import os
import time
from datetime import datetime
from urllib.parse import quote_plus

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "please-change-this-secret")

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "angelo")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "angelo")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "angelo123")

quoted_password = quote_plus(POSTGRES_PASSWORD)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{POSTGRES_USER}:{quoted_password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def wait_for_db(retries=10, delay=2):
    for attempt in range(retries):
        try:
            db.session.execute("SELECT 1")
            return True
        except Exception:
            time.sleep(delay)
    return False


def init_db():
    if wait_for_db():
        db.create_all()
        app.logger.info("Base de datos PostgreSQL lista y tablas creadas")
    else:
        app.logger.error("No fue posible conectar con la base de datos PostgreSQL")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


with app.app_context():
    init_db()


@app.route("/")
def index():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("index.html", products=products)


@app.route("/product/new", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()
        stock = request.form.get("stock", "0").strip()

        if not name or not category:
            flash("El nombre y la categoría son obligatorios.", "danger")
            return redirect(url_for("create_product"))

        try:
            product = Product(
                name=name,
                category=category,
                description=description,
                price=float(price),
                stock=int(stock),
            )
            db.session.add(product)
            db.session.commit()
            flash("Producto creado con éxito.", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            db.session.rollback()
            flash(f"Error al guardar el producto: {exc}", "danger")
            return redirect(url_for("create_product"))

    return render_template("form.html", title="Agregar producto", product=None)


@app.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form.get("name", product.name).strip()
        product.category = request.form.get("category", product.category).strip()
        product.description = request.form.get("description", product.description).strip()
        product.price = float(request.form.get("price", product.price))
        product.stock = int(request.form.get("stock", product.stock))

        try:
            db.session.commit()
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            db.session.rollback()
            flash(f"Error al actualizar el producto: {exc}", "danger")
            return redirect(url_for("edit_product", product_id=product.id))

    return render_template("form.html", title="Editar producto", product=product)


@app.route("/product/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash("Producto eliminado.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Error al eliminar el producto: {exc}", "danger")

    return redirect(url_for("index"))


@app.route("/api/products")
def api_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return {"products": [product.to_dict() for product in products]}


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

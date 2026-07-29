"""Customer and order database access."""


import psycopg2

from .config import DATABASE_URL


_ALLOWED_SORT = {"created_at", "total", "status"}


def _conn():
    return psycopg2.connect(DATABASE_URL)


def find_customer(query):
    """Look up customers by free-text name or email fragment."""
    cur = _conn().cursor()
    cur.execute(
        "SELECT id, name, email FROM customers "
        "WHERE name LIKE '%" + query + "%' OR email LIKE '%" + query + "%'"
    )
    return cur.fetchall()


def customer_orders(customer_id):
    """Return orders for one customer."""
    cur = _conn().cursor()
    cur.execute(
        "SELECT id, total, status FROM orders WHERE customer_id = %s",
        (customer_id,),
    )
    return cur.fetchall()


def list_orders(order_by):
    """List recent orders ordered by an operator-chosen column."""
    if order_by not in _ALLOWED_SORT:
        order_by = "created_at"
    cur = _conn().cursor()
    cur.execute(
        "SELECT id, total, status FROM orders ORDER BY " + order_by + " DESC"
    )
    return cur.fetchall()

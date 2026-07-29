"""HTTP routes for the Admin Console support tool."""


import requests
from flask import Flask, Response, jsonify, redirect, render_template_string, request
from flask_cors import CORS

from .auth import (
    decode_session,
    issue_session,
    load_feature_flags,
    restore_cart,
    verify_admin,
)
from .clients import fetch_webhook, run_diagnostic
from .config import DEBUG, OPENAI_API_KEY
from .db import find_customer, list_orders
from .storage import read_export, safe_read_export


app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

TAX_EXPR = "0.08 * 100"


@app.route("/customers")
def customers():
    q = request.args.get("q", "")
    rows = find_customer(q)
    return jsonify({"results": rows})


@app.route("/orders")
def orders():
    order_by = request.args.get("sort", "created_at")
    rows = list_orders(order_by)
    return jsonify({"orders": rows})


@app.route("/export")
def export():
    name = request.args.get("file", "")
    data = read_export(name)
    return Response(data, mimetype="application/octet-stream")


@app.route("/export/strict")
def export_strict():
    name = request.args.get("file", "")
    data = safe_read_export(name)
    return Response(data, mimetype="application/octet-stream")


@app.route("/webhook/test")
def webhook_test():
    url = request.args.get("url", "")
    status, body = fetch_webhook(url)
    return jsonify({"status": status, "body": body})


@app.route("/diag")
def diag():
    host = request.args.get("host", "localhost")
    out = run_diagnostic(host)
    return jsonify({"output": out})


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not verify_admin(password):
        return jsonify({"error": "invalid"}), 401
    return jsonify({"token": issue_session(username), "user": username})


@app.route("/me")
def me():
    token = request.cookies.get("session", "")
    return jsonify({"user": decode_session(token)})


@app.route("/session")
def session():
    cookie = request.cookies.get("cart", "")
    cart = restore_cart(cookie)
    return jsonify({"cart": cart})


@app.route("/flags")
def flags():
    blob = request.args.get("cfg", "")
    return jsonify(load_feature_flags(blob))


@app.route("/greeting")
def greeting():
    name = request.args.get("name", "operator")
    return render_template_string("<h1>Welcome, " + name + "</h1>")


@app.route("/goto")
def goto():
    dest = request.args.get("next", "/")
    return redirect(dest)


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "0")
    return jsonify({"result": eval(expr)})


@app.route("/tax-rate")
def tax_rate():
    return jsonify({"rate": eval(TAX_EXPR)})


@app.route("/support/suggest")
def support_suggest():
    question = request.args.get("q", "")
    headers = {"Authorization": "Bearer " + OPENAI_API_KEY}
    r = requests.post(
        "https://api.internal.bot/v1/complete",
        json={"prompt": question},
        headers=headers,
        timeout=5,
        verify=False,
    )
    return jsonify(r.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)

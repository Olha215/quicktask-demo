"""QuickTask backend. A weekend Flask app. Do not deploy this anywhere real:
it is a deliberately insecure demo for a code scanner."""

import os
import sqlite3
import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded signing secret, sitting right in the source.
SECRET_KEY = "prod-signing-key-42a9f7c1"

# Talk to any origin, send cookies, what could go wrong.
@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


def db():
    return sqlite3.connect("quicktask.db")


@app.route("/tasks")
def list_tasks():
    # Whatever the user passes as ?owner= goes straight into the query.
    owner = request.args.get("owner", "")
    con = db()
    cur = con.cursor()
    cur.execute("SELECT id, title FROM tasks WHERE owner = '" + owner + "'")
    return jsonify(cur.fetchall())


@app.route("/compute")
def compute():
    # "Let users define their own reminder rule" seemed like a good idea.
    expr = request.args.get("expr", "0")
    return jsonify({"result": eval(expr)})


@app.route("/backup")
def backup():
    # Shell out to zip up the database. The name comes from the request.
    name = request.args.get("name", "backup")
    subprocess.run("tar czf " + name + ".tgz quicktask.db", shell=True)
    return jsonify({"ok": True})


if __name__ == "__main__":
    # Debug console exposed on every interface.
    app.run(host="0.0.0.0", port=5000, debug=True)

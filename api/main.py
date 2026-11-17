from flask import Flask, request
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
conn_str = os.environ["DATABASE_URL"]

app = Flask(__name__)


@app.route("/api/get_shape")
def get_shape():
    sharpness: float = float(request.args.get("sharpness", -1.0))
    curviness: float = float(request.args.get("curviness", -1.0))
    confusion: float = float(request.args.get("confusion", -1.0))
    precision: float = float(request.args.get("precision", -1.0))

    return ""


@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()

    if (
        not data
        or "name" not in data
        or "accuracy" not in data
        or "time" not in data
    ):
        return {"error": "Incomplete request"}, 400

    return {"message": "Score submitted"}, 201


@app.route("/api/leaderboard")
def leaderboard():
    return {}, 200


@app.route("/api/has_user", methods=["POST"])
def has_user():
    data = request.get_json()

    if (
        not data
        or "name" not in data
    ):
        return {"error": "Incomplete request"}, 400

    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM RoundRecord WHERE username = %s;",
                (data["name"])
            )
            # If username doesn't exist, cur.fetchone() will return None
            if (cur.fetchone()):
                return {"result": True}, 200
            else:
                return {"result": False}, 200

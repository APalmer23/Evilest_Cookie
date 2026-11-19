from flask import Flask, request, render_template
import psycopg
import os
import random
from dotenv import load_dotenv

load_dotenv()
conn_str = os.environ["DATABASE_URL"]

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/get_shape")
def get_shape():
    # sharpness: float = float(request.args.get("sharpness", -1.0))
    # curviness: float = float(request.args.get("curviness", -1.0))
    # confusion: float = float(request.args.get("confusion", -1.0))
    # precision: float = float(request.args.get("precision", -1.0))
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM Shapes WHERE id = %s",
                (random.randint(0, 99), "")
            )
            results = cur.fetchone()

            if results:
                return {"shape": results[0], "shape_id": results[1]}, 200
    return {"error": "Invalid request"}, 400


@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()

    if (
        not data
        or "name" not in data
        or "accuracy" not in data
        or "time" not in data
        or "shape_id"
    ):
        return {"error": "Incomplete request"}, 400

    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT confusion, precision FROM Shapes WHERE id = %s
                """, (data["shape_id"])
            )
            shape_data = cur.fetchone()

            score = (data["accuracy"] * (shape_data[0] + shape_data[1]) / data["time"])

            cur.execute(
                """
                INSERT INTO RoundRecord
                (shape_id, accuracy, username, time, score)
                VALUES (%f, %f, %f, %f, %f)
                """, (
                    data["shape_id"],
                    data["accuracy"],
                    data["name"],
                    data["time"],
                    score
                )
            )

    return {"message": "Score submitted"}, 201


@app.route("/api/leaderboard")
def leaderboard():
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT ON(id) username, score
                FROM RoundRecord
                ORDER BY score DESC
                LIMIT 10
                """
            )
            results = cur.fetchall()
            return {"result": results}, 200
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

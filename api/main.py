from flask import Flask, request

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

    return {}, 200

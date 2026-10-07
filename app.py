"""Flask entry point for the Password Strength & Security Analyzer."""

from flask import Flask, jsonify, render_template, request

from analyzer.password_analyzer import analyze_password
from analyzer.password_generator import generate_password

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("password"), str):
        return jsonify({"error": "Request JSON must contain a password string."}), 400

    # Do not log, persist, or echo the password. It is passed directly to the
    # in-memory analysis function and goes out of scope after this request.
    return jsonify(analyze_password(payload["password"]))


@app.get("/api/generate")
def generate():
    try:
        length = int(request.args.get("length", 16))
        options = {
            "uppercase": request.args.get("uppercase", "true").lower() == "true",
            "lowercase": request.args.get("lowercase", "true").lower() == "true",
            "numbers": request.args.get("numbers", "true").lower() == "true",
            "symbols": request.args.get("symbols", "true").lower() == "true",
        }
        password = generate_password(length, options)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"password": password, "length": len(password)})


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request is too large."}), 413


if __name__ == "__main__":
    app.run(debug=False)

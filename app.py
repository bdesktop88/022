from flask import Flask, request, jsonify, render_template
import requests
import base64
import os

app = Flask(__name__, template_folder="templates")

RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET", "6LcBjT4rAAAAANCGmLJtAqAiWaK2mxTENg93TI86")


def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": RECAPTCHA_SECRET,
        "response": token
    }
    r = requests.post(url, data=data)
    return r.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/verify_recaptcha_init", methods=["POST"])
def verify_recaptcha_init():
    token = request.form.get("token")
    email_base64 = request.form.get("x")

    if not token or not email_base64:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    result = verify_recaptcha(token)

    if result.get("success"):
        return jsonify({"status": "success", "data": {"score": result.get("score", 0)}})
    else:
        return jsonify({"status": "error", "message": "reCAPTCHA failed"}), 403


@app.route("/_0x35adc6", methods=["POST"])
def handle_redirect():
    token = request.form.get("token")
    email_base64 = request.form.get("x")

    if not token or not email_base64:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    result = verify_recaptcha(token)
    if not result.get("success"):
        return jsonify({"status": "error", "message": "reCAPTCHA failed"}), 403

    try:
        email = base64.b64decode(email_base64).decode()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid Base64"}), 400

    redirect_url = f"https://example.com/thankyou?email={email}"
    return jsonify({"status": "success", "data": {"i": redirect_url}})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


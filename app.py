"""
LSB Steganography Tool - Flask Web Application
Run with: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, send_file, jsonify
from steganography import encode, decode, get_capacity
import os
import uuid
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encode", methods=["POST"])
def encode_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    message = request.form.get("message", "")
    password = request.form.get("password", None) or None

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Save uploaded file
    filename = f"{uuid.uuid4()}.png"
    input_path = os.path.join(UPLOAD_FOLDER, f"input_{filename}")
    output_path = os.path.join(UPLOAD_FOLDER, f"output_{filename}")
    file.save(input_path)

    try:
        encode(input_path, message, output_path, password)
        return send_file(output_path, as_attachment=True, download_name="encoded_image.png")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


@app.route("/decode", methods=["POST"])
def decode_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    password = request.form.get("password", None) or None

    filename = f"{uuid.uuid4()}.png"
    input_path = os.path.join(UPLOAD_FOLDER, f"dec_{filename}")
    file.save(input_path)

    try:
        result = decode(input_path, password)
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


@app.route("/capacity", methods=["POST"])
def capacity_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filename = f"{uuid.uuid4()}.png"
    input_path = os.path.join(UPLOAD_FOLDER, f"cap_{filename}")
    file.save(input_path)

    try:
        cap = get_capacity(input_path)
        return jsonify({"capacity": cap})
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

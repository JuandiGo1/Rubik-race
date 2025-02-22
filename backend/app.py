from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solver import resolver_rubik_race

import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subir un nivel
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if "inicial" not in request.files or "meta" not in request.files:
            return jsonify({"error": "Faltan archivos"}), 400

        inicial = request.files["inicial"].read().decode("utf-8")  # Leer en memoria
        meta = request.files["meta"].read().decode("utf-8")  # Leer en memoria

        # Enviar directamente los datos a la función sin guardarlos en disco
        solucion = resolver_rubik_race(inicial, meta)

        if solucion is None:
            return jsonify({"error": "No se pudo resolver el puzzle"}), 400

        return jsonify({"solucion": solucion})

    except Exception as e:
        print(f"Error en /upload: {e}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
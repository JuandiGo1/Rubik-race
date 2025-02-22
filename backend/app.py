from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from solver import resolver_rubik_race
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subir un nivel
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://127.0.0.1:8080"]}})
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'inicial' not in request.files or 'meta' not in request.files:
        return jsonify({'error': 'Faltan archivos'}), 400

    inicial = request.files['inicial']
    meta = request.files['meta']

    inicial_path = os.path.join(UPLOAD_FOLDER, "inicial.txt")
    meta_path = os.path.join(UPLOAD_FOLDER, "meta.txt")

    inicial.save(inicial_path)
    meta.save(meta_path)

    solucion_path = resolver_rubik_race(inicial_path, meta_path)

    if solucion_path is None or not os.path.exists(solucion_path):
        print(f"Error: No se encontró el archivo de salida en {solucion_path}")
        return jsonify({"error": "No se pudo resolver el puzzle o el archivo de salida no se generó"}), 400

    print(f"Abriendo archivo de solución en: {solucion_path}")
    
    try:
        with open(solucion_path, "r", encoding="utf-8") as file:
            solucion = json.load(file)  # Leer como JSON
        response = jsonify(solucion)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    except Exception as e:
        print(f"Error al abrir {solucion_path}: {e}")
        return jsonify({"error": f"No se pudo leer el archivo de salida: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
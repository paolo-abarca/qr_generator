from flask import Flask, render_template, request, jsonify
import qrcode

app = Flask(__name__)

# Función para cargar los cuadros del logo desde static/logo.txt
def cargar_logo():
    try:
        with open("static/logo.txt", "r", encoding="utf-8") as f:
            return f.read().split("...")  # Separar cuadros por '---'
    except FileNotFoundError:
        return ["ERROR: No se encontró el archivo logo.txt"]

logo_frames = cargar_logo()  # Cargar el logo en memoria

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_qr():
    data = request.form["data"]
    qr = qrcode.make(data)
    qr_path = "static/qr.png"
    qr.save(qr_path)
    return jsonify({"qr_path": qr_path})

@app.route("/get_logo_frame/<int:frame>")
def get_logo_frame(frame):
    frame %= len(logo_frames)  # Evita desbordamiento
    return jsonify({"logo": logo_frames[frame]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

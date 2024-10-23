import random

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from functools import wraps
import os

from services.card_recognition import recognize_card_from_image

app = Flask(__name__)
# Diretório para armazenar as imagens
UPLOAD_FOLDER = "uploads"
RECOGNIZE_FOLDER = f"{UPLOAD_FOLDER}/recognize"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RECOGNIZE_FOLDER"] = RECOGNIZE_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Usuário e senha para autenticação simples
USERNAME = "admin"
PASSWORD = "password"


# Função para verificar se o arquivo tem uma extensão permitida
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Decorator para exigir autenticação básica
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return jsonify({"message": "Authentication required"}), 401


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# Endpoint para upload de imagens
@app.route("/upload", methods=["POST"])
@requires_auth
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return (
            jsonify({"message": "File successfully uploaded", "filename": filename}),
            201,
        )
    else:
        return jsonify({"message": "Invalid file type"}), 400


# Endpoint para exibir todas as imagens enviadas
@app.route("/images")
def show_images():
    image_list = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("images.html", images=image_list)


@app.route("/images/json")
def show_images_json():
    image_list = os.listdir(app.config["UPLOAD_FOLDER"])
    """
    [
        {"photo_1729642334264.jpg": "http://127.0.0.1:5000/uploads/photo_1729642334264.jpg"},
    ]
    """
    image_list_dict = [
        {"filename": image, "url": f"{request.url_root}uploads/{image}"}
        for image in image_list
    ]
    return jsonify(image_list_dict)


# Endpoint para servir as imagens
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/card/recognize", methods=["POST"])
@requires_auth
def card_reconize():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["RECOGNIZE_FOLDER"], filename))
        print(f"File saved: {file}")
        file_path = os.path.join(app.config["RECOGNIZE_FOLDER"], filename)
        print(f"File path: {file_path}")
        response = recognize_card_from_image(file_path)
        return jsonify(response), 201
    else:
        return jsonify({"message": "Invalid file type"}), 400


# Página inicial (redireciona para a página de imagens)
@app.route("/")
def index():
    return redirect(url_for("show_images"))


@app.route("/ping")
def ping():
    # randon int
    return jsonify({"message": f"pong {random.randint(1, 100)}"})


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Faz o servidor Flask escutar em todas as interfaces de rede
    app.run(host="0.0.0.0", port=5000, debug=True)

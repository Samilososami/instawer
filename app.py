from flask import Flask, render_template, request, url_for
import instaloader
import requests
import os

app = Flask(__name__)

# Crear la carpeta "static" si no existe
if not os.path.exists("static"):
    os.makedirs("static")

def get_instagram_profile_pic(username):
    """ Obtiene la URL de la foto de perfil de Instagram y la guarda localmente """
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        img_url = profile.profile_pic_url  # URL de la foto de perfil
        img_path = f"static/{username}.jpg"

        # Descargar la imagen y guardarla
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as handler:
            handler.write(img_data)

        return img_path  # Retorna la ruta local de la imagen
    except Exception as e:
        print("Error obteniendo la imagen:", e)
        return None  # Si falla, retorna None

@app.route("/", methods=["GET", "POST"])
def home():
    profile_pic = None
    username = None

    if request.method == "POST":
        username = request.form["username"].strip()
        profile_pic = get_instagram_profile_pic(username)

        # Si no se pudo descargar la imagen, usa una imagen por defecto
        if not profile_pic:
            profile_pic = url_for('static', filename='default.jpg')

    return render_template("index.html", username=username, profile_pic=profile_pic)

if __name__ == "__main__":
    app.run(debug=True)

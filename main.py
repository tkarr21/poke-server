import os
from flask import Flask, send_file, request
from io import BytesIO
from createPoke import create 

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "Poke_Maker")
    return f"Hello this is the Poke_maker web service. make a request with the pokemon inputs to the generate endpoint"


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route("/generate", methods=["GET"] )
def generate_poke():
    try:
        args = request.args or {}
        img, gray_image, colored = create(args['hp'], args['attack'], args['defense'], args['sp_attack'], args['sp_defense'], args['speed'], args['type'])

        return serve_pil_image(img)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
)
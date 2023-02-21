import os
from flask import Flask, send_file, request
from flask_cors import CORS
from io import BytesIO
import json
from createPoke import create 
from describePoke import create_description
from PIL import Image
import base64

import pprint

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)

app = Flask(__name__)
CORS(app)

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

@app.route("/describe", methods=["POST"])
def generate_description():
    try:
        # read requets data as json
        data_as_dictionary = json.loads(request.data)
        # parse bytes from data url
        image_bytes = data_as_dictionary['data'][22:]
        # decode bytes to image
        im = Image.open(BytesIO(base64.b64decode(image_bytes)))
        # generate description
        description = create_description(model_name="models/vit-base-patch16-224-in21k-gpt2-finetuned-to-pokemon-descriptions-oak", image_ref=im)

        return description  
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}, 400


if __name__ == "__main__":
    #app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
)
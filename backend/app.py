import os
from flask import Flask, flash, request, redirect, url_for, session, request,  jsonify, Markup, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from flask_mongoengine import MongoEngine
from templates.template_pdf import generate_pdf
from templates.template_txt import generate_txt
#from AI.sound_to_text import get_audio_transcription
from AI.img_to_text import extract_text_img
import AI.extract_Ingredients as extr_ing
import AI.extract_Procedure as extr_proc
from AI.process_video import convert_video_to_audio
import io

import traceback

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = os.getcwd() + "\\uploads" #'/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['mp4'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Database 
app.config.update({
    "MONGODB_SETTINGS": {
        'db': os.environ.get("MONGO_DATABASE", "recipes"),
        'host': os.environ.get("MONGO_HOST", "127.0.0.1"),
        'port': int(os.environ.get("MONGO_PORT", 27017)),
        #'username': os.environ.get("MONGO_USER"),
        #'password': os.environ.get("MONGO_PASSWORD"),
    },
})
db = MongoEngine()

try:
    db.init_app(app)
except Exception:
    pass

class Recipes(db.Document):
    recipe_name = db.StringField() # recipe_name: The name of the recipe. (String)
    prep_time = db.IntField() # prep_time: The amount of time required to prepare the recipe. (Integer)
    cook_time = db.IntField() # cook_time: The amount of time required to cook the recipe. (Integer)
    total_time = db.IntField() # total_time: The total amount of time required to prepare and cook the recipe. (Integer)
    servings = db.IntField() # servings: The number of servings the recipe yields. (Integer)
    ingredients = db.ListField() # ingredients: A list of ingredients required to make the recipe. (List)
    tips = db.ListField() # tips: A list of tips to make the recipe. (List)
    directions = db.ListField() # directions: A list of directions for preparing and cooking the recipe. (List)
    rating = db.FloatField() # rating: The recipe rating. (Float)
    url = db.URLField( unique=True ) # url: The recipe URL. (String)
    cuisine_path = db.StringField() # cuisine_path: The recipe cuisine path. (String)
    nutrition = db.DictField() # nutrition: The recipe nutrition information. (Dictionary)
    timing = db.DictField() # timing: The recipe timing information. (Dictionary)
    is_mexican = db.BooleanField(default=False) # is_mexican: The recipe is mexican Boolean
    legals = db.BooleanField(default=False) # legals: the user accept the use of personal recipe


'''Funciones internas'''

#buscamos si la url de la receta ya ha sido procesada
def get_recipe_url(url : str):
    try:
        recipe = Recipes.objects(url=url).first()
        return recipe
    except Exception:
        return False


#consultamos por id para descargar la receta
def get_recipe_id(id : id):
    try:
        recipe = Recipes.objects(id=id).first()
        return jsonify(recipe)
    except Exception:
        return False

#generamos el archivo correspondiente
def generate_file(file_type, data):
    try:
        file = None
        f_type = ""

        if file_type == 'pdf':
            file = generate_pdf(data)
            f_type = "application/pdf"
        else:
            file = generate_txt(data)
            f_type = "application/text"

        file_data = {"name": data["name"], "file": base64.b64encode(file).decode(), "type": f_type}
      
        return jsonify(file_data)

    except Exception as e:
        print("Ha ocurrido un error:", e)
        traceback.print_exc()
        return False


'''APIS'''


#listamos todas las recetas
@app.route("/api/list", methods=['GET'])
def get_recipes():
    try:
        recipes = Recipes.objects()
        return jsonify(recipes), 200
    except Exception:
        return jsonify({"error": 'ha ocurrido un error'}), 500
    


#generamos el archivo descargable
@app.route('/download-file', methods=['POST'])
def download_file():
    try:

        body = request.get_json()
        id_recipe = body.get("id")
        type_file = body.get("type_file")

        recipe = get_recipe_id(id_recipe)
        generate_file(type_file, recipe)

        return generate_file, 200

    except Exception:
        return jsonify({"error": 'ha ocurrido un error al descargar el archivo'}), 500


def process_video(video, type_file= "file"):
    # Se obtiene el texto del video con sonido
    try:

        print("::Convirtiendo sonido a texto...")
        sound_text = convert_video_to_audio(video, type_file)

        img_text = extract_text_img()
    except Exception as e:
        print("Ha ocurrido un error:", e)
        traceback.print_exc()
        return False

    text = None
    #se unen ambos textos, poniendo de primero img
    if len(img_text) > 0 or len(sound_text) > 0 :
        text = img_text +". "+ sound_text
    
    print("::El video ha sido procesado exitosamente...")
    
    # Se obtienen los ingredientes
    ingredients, update_text = extr_ing.extract_ingredients(text)
    print(ingredients)
    
    print("::Se esta extrayendo el procedimiento...")
    procedure = extr_proc.extract_procedure(update_text)
    print(procedure)

    if len(ingredients) > 0 and len(procedure) > 0:
        return {"name": "name TODO", "ingredients": ingredients, "procedure": procedure }

    else: 
        return False

    #TODO post procesamiento y extracci'on
    print("::procesamos el video")


#crear la receta
@app.route('/api/upload', methods=['POST'])
def add_recipe():

    try:
        #datos from user
        file = None
        data = None
        body = request.get_json()
        url = body.get("url") or  ""
        is_mexican = body.get("is_mexican") or  False
        legals = body.get("legals") or  False
        type_file = body.get("type_file") or 'pdf'
        file_upload = body.get("file_upload") or False

        print("::type_file", type_file)

        data = None
        url_DB = None
        response = None
        
        if file_upload:
            response = process_video(file_upload, "local")
          
        if url != "":
            url_DB = url
            exist = get_recipe_url(url)
            print("::exist", exist)

            if exist :
                print("::devolvemos el archivo de una vez")
                data  = {"name": exist.recipe_name, "ingredients": exist.ingredients, "procedure": exist.directions } 
                #generamos file
                file = generate_file(type_file, data)
                return file, 200
            else:
                print("::ejecutamos toda la IA")
                response = process_video(url, "url")
        
        if response:
            data = response

            if data :

                #almacenar en la bd 
                add_DB = Recipes( recipe_name= data["name"],
                                ingredients=data["ingredients"],
                    directions=  data["procedure"],
                    url=  url_DB,
                    is_mexican=  is_mexican,
                    legals= legals  
                )
                add_DB.save()
                print("::result", add_DB)
                if add_DB.id:
                    file = generate_file(type_file, data)

                    return file, 200

                else : 
                    return jsonify({"error": 'No se pudo guardar el item, intente de nuevo'})

        else:
            return jsonify({"error": 'no es una receta'}), 500

    except Exception as e:
        print("Ha ocurrido un error:", e)
        traceback.print_exc()
        return jsonify({"error": 'ha ocurrido un error'}), 500


def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="Whatever you wish too return"
    return response


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

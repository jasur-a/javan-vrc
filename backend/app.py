import os
from flask import Flask, flash, request, redirect, url_for, session, request,  jsonify, Markup
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from flask_mongoengine import MongoEngine
from templates.template_pdf import generate_pdf
from templates.template_txt import generate_txt
from AI.sound_to_text import SoundToText
import AI.extract_Ingredients as extr_ing
#import AI.extract_Procedure as extr_proc

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# load_dotenv()
# MONGO_URI = os.environ.get('MONGO_URI')



logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Database 
app.config.update({
    "MONGODB_SETTINGS": {
        'db': os.environ.get("MONGO_DATABASE", "recipes"),
        'host': os.environ.get("MONGO_HOST", "127.0.0.1"),
        'port': int(os.environ.get("MONGO_PORT", 27017)),
        'username': os.environ.get("MONGO_USER"),
        'password': os.environ.get("MONGO_PASSWORD"),
    },
})
db = MongoEngine(app)

try:
    db.init_app(app)
except Exception:
    pass

class Recipes(db.Document):
    recipe_name: db.StringField() # recipe_name: The name of the recipe. (String)
    prep_time: db.IntField() # prep_time: The amount of time required to prepare the recipe. (Integer)
    cook_time: db.IntField() # cook_time: The amount of time required to cook the recipe. (Integer)
    total_time: db.IntField() # total_time: The total amount of time required to prepare and cook the recipe. (Integer)
    servings: db.IntField() # servings: The number of servings the recipe yields. (Integer)
    ingredients: db.ListField() # ingredients: A list of ingredients required to make the recipe. (List)
    tips: db.ListField() # tips: A list of tips to make the recipe. (List)
    directions: db.ListField() # directions: A list of directions for preparing and cooking the recipe. (List)
    rating: db.FloatField() # rating: The recipe rating. (Float)
    url: db.URLField( unique=True ) # url: The recipe URL. (String)
    cuisine_path: db.StringField() # cuisine_path: The recipe cuisine path. (String)
    nutrition: db.DictField() # nutrition: The recipe nutrition information. (Dictionary)
    timing: db.DictField() # timing: The recipe timing information. (Dictionary)
    is_mexican: db.BooleanField(default=False) # is_mexican: The recipe is mexican Boolean
    legals: db.BooleanField(default=False) # legals: the user accept the use of personal recipe


# def add_recipe():
#     result = db.recipe.insert_one({
#         "recipe_name": ,
#         "prep_time": ,
#         "cook_time": ,
#         "total_time":,
#         "servings": ,
#         "ingredients": ,
#         "directions": ,
#         "rating",
#         "url":,
#         "cuisine_path": ,
#         "nutrition": ,
#         "timing": ,
#         "is_mexican": ,
#         "legals": , 
#         })
#     return str(result.inserted_id)

'''APIS'''

#listamos todas las recetas
@app.route("/api/list", methods=['GET'])
def get_recipes():
    try:
        recipes = Recipes.objects()
        return jsonify(recipes), 200
    except Exception:
        return jsonify({"error": 'ha ocurrido un error'}), 500
    


#buscamos si la url de la receta ya ha sido procesada
def get_recipe_url(url : str):
    try:
        recipe = Recipes.objects(url=url).first()
        print("::recipe", recipe)

        return jsonify(recipe), 200
    except Exception:
        return False


#consultamos por id para descargar la receta
def get_recipe_id(id : id):
    recipe = Recipes.objects(id=id).first()
    return jsonify(recipe), 200


@app.route('/download-file')
def download_file(type_file, data):
    print("::generamos el descargable")
    try:
        if type_file == 'pdf':
            file = generate_pdf(data)

            return file, 200
        else:
            file = generate_txt(data)

            return file, 200
    except Exception:
        return False


def process_video(video, type= "file"):
    # Se obtiene el texto del video con sonido
    #try:
    #    print("::Convirtiendo sonido a texto...")
    #    sound_to_text = SoundToText(video)
    #    sound_to_text.current_folder
    #    sound_to_text.convert_video_to_audio()
    #except Exception:
    #    return jsonify({"error": 'No se ha podido obtener el texto del video'}), 500

    
    print("::El video ha sido procesado exitosamente...")
    
    # Se obtienen los ingredientes
    ingredients = extr_ing.extract_ingredients()
    print(ingredients)
    
    print("::Se esta extrayendo el procedimiento...")
    #extr_proc
    
    #se unen ambos textos, poniendo de primero img

    #text = img_text + sound_text #TODO

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

        if 'fileUpload' in request.files:
            target=os.path.join(UPLOAD_FOLDER,'test_docs')
            file = request.files['fileUpload']
            print("::f", file)
            filename = secure_filename(file.filename)
            destination="/".join([target, filename])
            file.save(destination)
            session['uploadFilePath']=destination
            recipe = process_video(file)

        if url != "":
            exist = get_recipe_url(url)
            print("::exist", exist)

            if exist :
                print("::devolvemos el archivo de una vez")
                data  = {""} #TODO
                #generamos file
                file = download_file(type_file, data)
                return
            else:
                print("::ejecutamos toda la IA")
                data = process_video(url, "url")


        data  = {  "name" : "Receta de Chiles Poblanos",
            "ingredients" : [
                "10 chiles poblanos",
                "10 palitos de queso",
                "5 tomates ",
                "1 diente de ajo ",
                "poquita crema ",
                "pimienta negra",
                "jitomates ",
                "queso ",
                "atún ",
                "poquito aceite ",
                "poquita agua ",
                "poquita sal ",
                "1 rebanada de cebolla "
            ],
            "procedure" : [
                "1.- Hacer los chiles.",
                "2.- Desvenar estos chilitos guajillos.",
                "3.- Cocer los chilitos.",
                "4.- Poner una pimienta negra.",
                "5.- Quitar la pecatita.",
                "6.- Poner poquito de aceite.",
                "7.- Moler el chile y los jitomates.",
                "8.- Poner los jitomates, la cebolla y el ajo.",
                "9.- Poner la crema.",
                "10.- Poner poquita agua.",
                "11.- Poner poquita sal.",
                "12.- Poner una rebanada de cebolla.",
                "13.- Dejar que hierva bien.",
                "14.- Agregarle los chiles."
            ],
            "tips": []
        }

        #if data :
            #generamos file
            #file = download_file(type_file, data)

            #almacenar en la bd ...... TODO

       #     return file, 200#jsonify(movie), 201

        return jsonify({"error": 'No es una receta'}), 500

    except Exception:
        return jsonify({"error": 'ha ocurrido un error'}), 500

# @app.route('/upload', methods=['POST'])
# def fileUpload():
#     target=os.path.join(UPLOAD_FOLDER,'test_docs')
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     logger.info("welcome to upload`")
#     file = request.files['file'] 
#     filename = secure_filename(file.filename)
#     destination="/".join([target, filename])
#     file.save(destination)
#     session['uploadFilePath']=destination
#     response="Whatever you wish too return"
#     return response

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

#CORS(app, expose_headers='Authorization')

#https://medium.com/excited-developers/file-upload-with-react-flask-e115e6f2bf99
#https://github.com/plouc/mozaik/issues/118
#https://www.geeksforgeeks.org/how-to-connect-reactjs-with-flask-api/
#https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/
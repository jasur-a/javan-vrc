#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install opencv-python --upgrade setuptools wheel youtube_dl install pafy pytube pytesseract setuptools wheel spacy language_tool_python panda


# In[2]:


pip install pattern


# In[6]:


get_ipython().system('python3 -m spacy download es_core_news_lg')


# In[7]:


get_ipython().system('python3 -m pip install -U pip')


# In[8]:


pip install --upgrade setuptools


# In[9]:


pip install  openpyxl


# In[10]:


import cv2
import os
import numpy as np
import pytesseract
from pytesseract import Output
from pytube import YouTube
from PIL import Image, ImageEnhance
import pandas as pd

import spacy
from spacy.tokens import Token
import re
import language_tool_python

#from pattern.es import pluralize


# In[ ]:


import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# In[ ]:


#declaracion de las librerias de NPL
nlp = spacy.load("es_core_news_lg")
tool = language_tool_python.LanguageTool('es')



# In[ ]:


"""
Obtiene los ingredientes del dataset.
"""
def get_ingredients_from_file(dataset):
    return pd.read_excel(dataset)


# In[ ]:


"""
Define la palabra y la convierte a plural usando la función pluralize().
""" 
def to_plural(word):
    # #https://stackoverflow.com/questions/31387905/converting-plural-to-singular-in-a-text-file-with-python
    # Installing NLTK data to import
    # and run en module of pattern
    #nltk.download('popular')

    return pluralize(word)


# In[ ]:


"""
Define la palabra y la convierte a singular usando la función singularize().
""" 
def to_singular(word):
    # # Import the NLTK module https://www.geeksforgeeks.org/python-program-to-convert-singular-to-plural/
    return singularize(word)


# In[ ]:


"""
Obtiene los ingredientes del dataset.
"""
def get_ingredients_from_file(dataset):
    return pd.read_excel(dataset)


# In[ ]:


"""
Preprocesar información (se convierte la primera columna a minusculas y se eliminan NAN)
""" 
def get_ingredients(main_ingredient):
    basic_ingredients = main_ingredient.dropna().T.drop_duplicates().T

    ingredients = []
    for ing in basic_ingredients:
        #ingredients.append(to_plural(ing))
        #ingredients.append(to_singular(ing))
        
        ingredients.append(ing)
        
    return ingredients


# In[ ]:


main_ingredient = ingredients_set.iloc[:, 0].str.lower()


# In[ ]:


# Se obtienen los datos de los datasets
ingredients = get_ingredients(main_ingredient)


# In[ ]:


ingredients.append("tortillas")


# In[ ]:


'tortillas' in ingredients


# In[ ]:


'''evaluamos la semantica de la palabra para ver si esta correctamente formulada la oracion 
o hay textos basura, pero validos en español'''
def semantic(token):
    #validar si la estructura de la oracion no se cumple
    if token.pos_ in ['NUM', 'PUNCT', 'VERB', 'NOUN', 'ADJ', 'ADV', 'PROPN']:
        if (not token.is_alpha and token.pos_ not in ['NUM', 'PUNCT'] ) or (token.pos_ == 'PUNCT' and token.i == 0):
            return False
        return True
    else:
        return False

def consonant(token):
    alphabet_es = 'abcdefghijklmnñopqrstuvwxyz'
    vowels = 'aeiou'
    text = token.text.lower()
    return (text in alphabet_es) and (text not in vowels)


#evaluamos la sintaxis de la letra/palabra para ver si no es texto basura 
def syntax(token):
    if token._.is_ingredient:
        return True
    
    if token.is_oov or not token._.is_spanish:
        # Verificamos si la palabra es desconocida en el modelo o no es espa;ol
        return False
    
    if token.is_alpha and not token.is_stop :
        '''verificamos si el token es una palabra o no y si no es una palabra vacía 
        .is_alpha se utiliza para verificar si un token es una palabra o no.
        booleano que indica si el token es una palabra vacía o de stop. (y, a, la ....)'''

        if token._.is_semantic and not token._.is_consonant:
            '''validamos si es semanticamente correcto y si no es una vocal, asi devolvemos TRUE 
            a las palabras (que si cumplen con estas condiciones)'''
            return True
        
        return False
    
    return True


# Verificamos si la palabra existe en el vocabulario del modelo en ES
def spanish_word(token):
    if nlp.vocab.has_vector(token.text) or token._.is_ingredient:
        return True
    return False

def ingredient(token):
    return token.text.lower() in ingredients is not False

def symbol(token):
    # Expresión regular que busca cualquier caracter que no sea una letra, número o espacio en blanco
    patron = r'[^a-zA-Z1-9ñÑáéíóúÁÉÍÓÚüÜ\d\s/\d.]'
    # Buscamos el patrón en el texto
    res = re.search(patron, token.text)
    # Si se encuentra algún símbolo devuelve True
    return res is not False

#creamos nuestras propiedades personalizadas
Token.set_extension('is_semantic', getter=semantic, force=True)
Token.set_extension('is_syntax', getter=syntax, force=True)
Token.set_extension('is_spanish', getter=spanish_word, force=True)
Token.set_extension('is_consonant', getter=consonant, force=True)
Token.set_extension('is_symbol', getter=symbol, force=True)
Token.set_extension('is_ingredient', getter=ingredient, force=True)


# In[ ]:



def grammar_validate(sentence):
    matches = tool.check(sentence)
    if len(matches) > 0:
        #La oración tiene errores sintácticos.
        return False
    else:
        #La oración es gramaticalmente correcta.
        return True

def word_validate(sentence):
    doc_es = nlp(sentence)
    words =  []

    # Expresión regular que busca cualquier caracter que no sea una letra, número o espacio en blanco
    patron = r'[^a-zA-Z1-9ñÑáéíóúÁÉÍÓÚüÜ\d\s/\d.]'
    validate = ['NUM', 'PUNCT']

    is_valid = []
    have_ingredient = False

    black_list = ["ol", "ae", "cu", "re", "cis", "ea", "pe", '/']

    for token in doc_es:

        # Buscamos el patrón en el texto
        res = re.search(patron, token.text)

        # Si se encuentra algún símbolo devuelve True
        is_symbol = res is not None


        print(token.text, " alpha:", token.is_alpha, " stop: " , token.is_stop, " desconocida: ", token.is_oov, token.pos_)
        print("    sem:", token._.is_semantic,  "syntax:", token._.is_syntax, "spanish:", token._.is_spanish, " is_consonant", token._.is_consonant, "is_ingredient", token._.is_ingredient, "is_symbol", is_symbol )



        if not is_symbol:
            print("::NO es simbolo")
            if token.text in black_list :
                continue
            
            if token._.is_ingredient:
                have_ingredient = True
                words.append(token.text.capitalize())
                is_valid.append(True)
                continue

            #if token.tag_ not in validate:

                #is_spanish = spanish_word(token)
                #is_valid = all([token._.is_semantic, token._.is_spanish, token._.is_syntax])

                #if is_valid :
                #    words.append(token.text)
            #else:
            #    words.append(token.text)

            if all([token._.is_semantic, token._.is_spanish, token._.is_syntax]):
                words.append(token.text)
                is_valid.append(True)
                continue
        # else:
        #     is_valid.append(False)


    # if have_ingredient : 

    #     print( )
    #     return ' '.join(words)
    
    
    # if all([valid for valid in is_valid]):
    #     return ' '.join(words)
    # else:
    #     return None

        #print("La oración es inválida.")
    
    sentence = ' '.join(words)
    grammar  = grammar_validate(sentence)
    print("::" , sentence, "word",  words, "::grammar:", grammar)
    
    if not grammar:
        return None
    return sentence


# In[ ]:


class Video:
    def __init__(self, path, url):
        self.path = path
        self.videoUrl = url
        self.yt = self.Download()
        #self.localUrl = ''
        #self.yt = ''
        
    def Download(self):
        #por ahora para archivos de internet
        file = self.Network()
        print(file)
        return file

    def Network(self):
        yt = YouTube(self.videoUrl)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        localUrl = yt.download(self.path)
        self.localUrl = localUrl
        return yt

#'https://www.youtube.com/watch?v=REAFtXGnpKU'


# In[ ]:



video = Video('C:/Users/jasura/Documents/maestria/seminario',
 'https://www.youtube.com/watch?v=XE6epSyQrkw' )


# In[ ]:


video.localUrl


# In[ ]:


def img_process(img):

    #convertimos a RGB
    # color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  
    # # Displaying the converted image
    # image = Image.fromarray(color_coverted)

    # # agregado de sharpness y contrast a la  imagen
    # enhancer1 = ImageEnhance.Sharpness(image)
    # enhancer2 = ImageEnhance.Contrast(image)
    # img_edit = enhancer1.enhance(20.0)
    # img_edit = enhancer2.enhance(1.5)

    # cv_img = cv2.cvtColor(np.array(img_edit), cv2.COLOR_RGB2BGR)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar una operación morfológica para eliminar el ruido
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    
    # Aplicar una operación de threshold para aumentar el contraste
    thresh = cv2.threshold(opening, 200, 255, cv2.THRESH_BINARY_INV)[1]
    #plt.imshow(thresh);
    # Encontrar contornos en la imagen thresholdada
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializar una lista para almacenar los rectángulos que contienen el texto
    rects = []
    
    # Recorrer cada contorno
    for cnt in contours:
        # Obtener el rectángulo que encierra el contorno
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Agregar el rectángulo a la lista si cumple con ciertos criterios
        if w > 50 and h > 50:
            rects.append((x, y, w, h))


    # Recorrer cada rectángulo
    for rect in rects:
        x, y, w, h = rect
        roi = thresh[y:y+h, x:x+w]
        
    #convertimos a RGB
    #color_coverted = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
  
    # Displaying the converted image
    pil_image = Image.fromarray(roi)

    return pil_image


# In[ ]:


def extract_text_img(img):
    
    image = img_process(img)

    # Utilizar OCR (Reconocimiento Óptico de Caracteres) para extraer el texto de la región de interés
    ocr = pytesseract.image_to_string(image)

    print(ocr, len(ocr))


    ocr_validate = word_validate(ocr.lower())

    print("::ocr_validate", ocr_validate)
    if not ocr_validate:
        return None

    #print(text)
    return ocr_validate


# In[ ]:


cam = cv2.VideoCapture(video.localUrl)


# In[ ]:



complete_text = []
prev_text = ""

# Establecer un nivel mínimo de similitud exigido:
nivel_minimo = 0.8



while(cam.isOpened()):
    # Leer el siguiente fotograma
    ret, frame = cam.read()

    # color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
    
    # # Displaying the converted image
    # pil_image = Image.fromarray(color_coverted)

    # Si no hay más fotogramas, salir del bucle
    if not ret:
        break

    # Validamos que la imagen no sea 100% negra
    is_black = not np.any(frame)

    #si la img es negra ignoramos
    if is_black:
        continue

    # Utilizar funcion extract_text extraer el texto de la imagen
    text = extract_text_img(frame)


    if text :


        print(prev_text," - ", text)
        # Obtener el objeto Doc para cada texto:
        pt = nlp(prev_text)
        nt = nlp(text)

        # Calcular la similitud entre los textos:
        similitud = pt.similarity(nt)

        #TODO agregar todos los coincidentes en un array y luego seleccionar el que tenga mas letras, si se comparte la misma cantidad con otro solo se  seleccionara 1


        if similitud >= nivel_minimo:
            #print('Los textos son similares.')
            continue
        else:
            #print('Los textos no son suficientemente similares.')
            prev_text = text
            complete_text.append(text)
    
    # Imprimir el texto extraído

print(' '.join(complete_text))
# Liberar la cámara
cam.release()


# In[ ]:


complete_text


# In[ ]:


prev_text


# In[ ]:


print(' '.join(complete_text))


# In[ ]:


def word_validate2(sentence):
    doc_es = nlp(sentence)
    words =  []

    # Expresión regular que busca cualquier caracter que no sea una letra, número o espacio en blanco
    patron = r'[^a-zA-Z1-9ñÑáéíóúÁÉÍÓÚüÜ\d\s/\d.]'
    validate = ['NUM', 'PUNCT']

    is_valid = []
    have_ingredient = False

    for token in doc_es:

        # Buscamos el patrón en el texto
        res = re.search(patron, token.text)

        # Si se encuentra algún símbolo devuelve True
        is_symbol = res is not None


        print(token.i, token.text, " alpha:", token.is_alpha, " stop: " , token.is_stop, " desconocida: ", token.is_oov, "token.tag_", token.tag_ , "token.pos_", token.pos_, "token.dep_", token.dep_)
        print("    sem:", token._.is_semantic,  "syntax:", token._.is_syntax, "spanish:", token._.is_spanish, " is_consonant", token._.is_consonant, "is_ingredient", token._.is_ingredient, "is_symbol", is_symbol )


        if not is_symbol:
            print("::NO es simbolo")
            if token.text == '/':
                continue
            if token._.is_ingredient:
                have_ingredient = True
                words.append(token.text.capitalize())
                is_valid.append(True)
                continue

            #if token.tag_ not in validate:

                #is_spanish = spanish_word(token)
                #is_valid = all([token._.is_semantic, token._.is_spanish, token._.is_syntax])

                #if is_valid :
                #    words.append(token.text)
            #else:
            #    words.append(token.text)

            if all([token._.is_semantic, token._.is_spanish, token._.is_syntax]):
                words.append(token.text)
                is_valid.append(True)
                continue
        # else:
        #     is_valid.append(False)


    # if have_ingredient : 

    #     print("::" , sentence, "word",  words )
    #     return ' '.join(words)
    
    
    # if all([valid for valid in is_valid]):
    #     return ' '.join(words)
    # else:
    #     return None

        #print("La oración es inválida.")
    
    sentence = ' '.join(words)
    grammar  = grammar_validate(sentence)
    print("::grammar:", grammar, words)
    
    if not grammar:
        return None
    return sentence


# In[ ]:


ocr_validate = word_validate2(',')


# In[ ]:


nlp.vocab.has_vector("Tatemar")


# In[ ]:


grammar_validate('Tatemar')


# In[ ]:


'mexicanas',
 'Tortillas',
 'Tortillas mexicanas',
 '4 Tortillas',


# In[ ]:


# Obtener el objeto Doc para cada texto:
pt = nlp('Tortillas mexicanas')
nt = nlp('4 Tortillas')

# Calcular la similitud entre los textos:
pt.similarity(nt)


# In[ ]:


def add_punct(token):
    if 


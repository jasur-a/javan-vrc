#!/usr/bin/env python
# coding: utf-8

import cv2
import os
import numpy as np
import pytesseract
from pytesseract import Output
from pytube import YouTube
from PIL import Image, ImageEnhance
import pandas as pd
import os, shutil

import re
import language_tool_python

from AI.process_text import Doc, word_validate

#declaracion de las librerias de NPL
tool = language_tool_python.LanguageTool('es')


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



#video = Video(os.getcwd(),
# 'https://www.youtube.com/watch?v=XE6epSyQrkw' )



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


def extract_text(img):

    image = img_process(img)

    # Utilizar OCR (Reconocimiento Óptico de Caracteres) para extraer el texto de la región de interés
    ocr = pytesseract.image_to_string(image)

    print("::ocr", ocr)
    if len(ocr) > 0 :

        ocr_validate = word_validate(ocr.lower())

        if not ocr_validate:
            return None

        #print(text)
        return ocr_validate
    
    return ""


def extract_text_img():


    url = os.getcwd() + "/Converted_results/" + "Chiles Rellenos sin Capear De Mi Rancho A Tu Cocina.mp4"

    cam = cv2.VideoCapture(url)

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
        text = extract_text(frame)


        if text :

            print(prev_text," - ", text)
            # Obtener el objeto Doc para cada texto:
            pt = Doc(prev_text)
            nt = Doc(text)

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

    return ' '.join(complete_text)
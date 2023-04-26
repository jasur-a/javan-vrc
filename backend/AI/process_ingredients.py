#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import nltk
#nltk.download()

import spacy
from spacy.tokens import Token
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


# Otras librerías
import os, shutil
import pandas as pd
import json
import re

from itertools import islice

from pattern.es import pluralize
from pattern.es import singularize



"""
Define la palabra y la convierte a plural usando la función pluralize().
""" 
def to_plural(word):
    # #https://stackoverflow.com/questions/31387905/converting-plural-to-singular-in-a-text-file-with-python
    # Installing NLTK data to import
    # and run en module of pattern
    #nltk.download('popular')

    return pluralize(word)


"""
Define la palabra y la convierte a singular usando la función singularize().
""" 
def to_singular(word):
    # # Import the NLTK module https://www.geeksforgeeks.org/python-program-to-convert-singular-to-plural/
    return singularize(word)



"""
Obtiene los ingredientes del dataset.
"""
def get_ingredients_from_file(excelFile):
    path = os.getcwd() + "/datasets/" + excelFile
    print("::path", path)
    file_to_read = Path(path)
    if not file_to_read.exists():
        print("File not exists")

    with file_to_read.open('rb') as file:
        try:
            print("Leyendo dataset de ingredientes")
            return pd.read_excel(file, engine='openpyxl')
        except ModuleNotFoundError as e:
            print('Could not load previous results')


"""
Preprocesar información (se convierte la primera columna a minusculas y se eliminan NAN)
""" 
def get_ingredients(main_ingredient):
    basic_ingredients = main_ingredient.dropna().T.drop_duplicates().T

    ingredients = []
    for ing in basic_ingredients:
        ingredients.append(to_plural(ing))
        ingredients.append(to_singular(ing))
        
    return ingredients

"""
Se obtienen los datos de un archivo json.
"""
def parse_json_file(jsonfile):
    path = os.getcwd() + "/datasets/" + jsonfile
    file_to_read = Path(path)
    if not file_to_read.exists():
        print("File not exists")
    with file_to_read.open('rb') as file:
        try:
            print("Leyendo dataset...")
            measures_content = file.read()
            parsed_json = json.loads(measures_content)
            return parsed_json
        except ModuleNotFoundError as e:
            print('Could not load previous results')
            return False


"""
Obtiene las medidas del dataset.
""" 
def get_measures_from_file(jsonfile):
    measures_set = []
    
    parsed_json = parse_json_file(jsonfile)
    
    for liq_items in parsed_json['liquidos']:
        measures_set.append(liq_items)

    for sol_items in parsed_json['solido']:
        measures_set.append(sol_items)
    
    return measures_set


# Une los ingredientes con sus respectivos complementos descriptivos. #TODO eliminar
def merge_ingredients_with_description(main_ingredient, complementary1, complementary2):
    data = []
    data = main_ingredient + (' ' + complementary1).fillna('') + (' ' + complementary2).fillna('')
    return data



def ingredients():
    #Se obtienen los ingredientes y las tres primeras columnas.
    ingredients_set = get_ingredients_from_file('ingredientes.xlsx')
    print(ingredients_set)

    main_ingredient = ingredients_set.iloc[:, 0].str.lower()
    complementary1  = ingredients_set.iloc[:, 1].str.lower()
    complementary2  = ingredients_set.iloc[:, 2].str.lower()
    
    merge_ingredients_with_description(main_ingredient, complementary1, complementary2)
    
    # Se obtienen los datos de los datasets
    return get_ingredients(main_ingredient)
#!/usr/bin/env python
# coding: utf-8

import sys

# Librerías para PNL
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

from AI.process_ingredients import ingredients, parse_json_file, get_measures_from_file

from AI.process_text import Doc, parse_text, get_tokenized_words, get_word_text, insert_punct

#nltk.download('popular')


"""
Cuando hay ingredientes en la descripcion se obtiene solo este texto
"""
def get_text_from_description(parse_text):
    from_description = []
    paragraph = []
    paragraphs = []
    
    for i, word in enumerate(parse_text):
        if word[0] != "descripción" or parse_text[i + 1][0] != "del" or parse_text[i + 2][0] != "video":
            continue
        for w in range(i + 2, len(parse_text)):
            if parse_text[w][0] == "ingredientes":
                for j in range(w + 1, len(parse_text)):
                    if parse_text[j][0] == ":":
                        continue
                    if "\n" in parse_text[j][0]:
                        paragraphs.append(paragraph)
                        paragraph = []
                        continue
                    paragraph.append(parse_text[j][0])
                    #from_description.append(parse_text[j][0])
     
    # Eliminar parrafos inncessarios
    copy_paragraphs = paragraphs.copy()
    for index, p in enumerate(paragraphs):
        p_tokens = Doc(" ".join(p))
        for token in p_tokens:
            if token.like_url:
                copy_paragraphs.pop(index)
                break
    
    from_description = []
    for pars in copy_paragraphs:
        for p in pars:
            from_description.append(p)
        from_description.append("\n")

    if len(from_description) == 0:
        return []
    else:  
        return from_description





"""
Clase que puede traducir cadenas de palabras numéricas 
comunes en espanol y convertirlas en la cantidad numérica correspondiente.
"""
class WordsToInt():
    # Asignación de dígitos a nombres relativos a unidades "ones".
    __ones__ = { 'un':   1, 'una':   1, 'uno':   1, 'once':     11,
                 'dos':   2, 'doce':     12,
                 'tres': 3, 'trece':   13,
                 'cuatro':  4, 'catorce':   14,
                 'cinco':  5, 'quince':    15,
                 'seis':   6, 'dieciseis':    16,
                 'siete': 7, 'diecisiete':  17,
                 'ocho': 8, 'dieciocho':   18,
                 'nueve':  9, 'diecinueve':   19,
                 'diez': 10
               }
    
    # Asignación de dígitos a nombres relativos 'decenas'.
    __tens__ = { 
                 'veinte':  20,
                 'treinta':  30,
                 'cuarenta':   40,
                 'cincuenta':   50,
                 'sesenta':   60,
                 'setenta': 70,
                 'ochenta':  80,
                 'noventa':  90 
    }
    
    # Asignación de dígitos a nombres relativos 'centenas'.
    __hundreds__ = {
                'cien': 100, 'ciento': 100,
                'quinientos': 500,
                'setecientos': 700,
                'mil':  1000,
    }
    
    # Lista ordenada de los nombres asignados a los grupos de miles.
    __groups__ = { 
                   'mil':  1000,
                   'millon':   1000000,
                   'billoon':   1000000000,
                   'trillon':  1000000000000 
    }
    
    # Asignación de dígitos a nombres relativos de 'fracciones'.
    __fraction__ = { 'medio':  2, 'media': 2, 'tercio': 5, 'cuarto': 4, "cuarta": 5 }

    # Expresión regular que busca nombres de grupos de números y captura:
    # 1- la cadena que precede al nombre del grupo, y
    # 2- el nombre del grupo (o una cadena vacía si el
    # el valor capturado es simplemente el final de la cadena
    # indicando el grupo 'unos', que normalmente es
    # no expresado)
    __groups_re__ = re.compile(
        r'\s?([\w\s]+?)(?:\s((?:%s))|$)' %
        ('|'.join(__groups__))
        )

    # Expresión regular que busca dentro de un solo grupo de números para
    # 'n cien' y captura:
    # 1- la cadena que precede de 'cientos', y
    # 2- la cadena que sigue al 'cientos'.
    # Se considerará como el número que indica el
    # valor posicional de las decenas y las unidades del grupo.
    __hundreds_re__ = re.compile(r'([\w\s]+)cientos(?:\s(.*)|$)')
    
    __hundreds_extra__ = re.compile(r'([\w]+)(?:\s(.*)|$)')

    # Expresión regular que se ve dentro de un solo número o
    # grupo al que ya se le extrajo su valor de 'cientos'
    # para un patrón de 'decenas' (es decir, 'cuarenta y dos') y captura:
    #1- las decenas
    #2- los unos
    __tens_and_ones_re__ =  re.compile(
        r'((?:%s))(?:\s(.*)|$)' %
        ('|'.join(__tens__.keys()))
        )
    
    # Expresión regular que busca dentro de un solo grupo de números para
    # 'fracción' y captura:
    # 1- el primer número ordinario (1)
    # 2- el nombre fraccionario (4)
    # Al final da 1/4
    __fraction_re__ = re.compile(
        r'\s?([\w\s]+?)(?:\s((?:%s))|$)' %
        ('|'.join(__fraction__))
        )

    """
    Analiza las palabras hasta encontrar número que describen.
    """
    def parse(self, words):
        # Se van a analizar las palabras con ciertos tags o lemas.
        
        words = words.lower().strip()
       
        # Crea una lista para guardar los grupos de números tal como los encontramos dentro
        # la cadena de palabras.
        groups = {}        
        # Crea una variable para guardar un número.
        num = 0
         
        # Se dividen las palabras para saber si existe algun número en las listas numéricas.
        split_words = words.split()
        updated_words = ""
        
        indexes = []
        found_words = []
        firstNumber = []
        
        for idx, word in enumerate(split_words):
            # Se tokeniza la palabra numérica.
            doc = Doc(word)
            
            tokenized_number = [[ w.pos_, w.lemma_, w.text] for w in doc][0]
            
            # Número no puede ser igual al anterior
            if idx > 0 and word == split_words[idx - 1]:
                continue
            
            if tokenized_number[0] == "NUM" or (tokenized_number[2] == "uno" or tokenized_number[2] == "un" or tokenized_number[2] != "unas" and tokenized_number[2] == "una") or tokenized_number[1] == "cuarto":
          #  if tokenized_number[0] == "NUM" or tokenized_number[2] == "cuarto" or (tokenized_number[2] == "uno" or tokenized_number[2] == "un" and tokenized_number[2] == "una"):
                updated_words += " " + word
            else:
                continue
        
        # Se crea nuevamente una cadena de texto más limpio.
        updated_words = updated_words.strip()
        
        # En caso de que una palabra contenga una fracción.
        has_fraction = [True for fr_word in split_words if fr_word in WordsToInt.__fraction__.keys()]
        
        if len(split_words) > 1 and len(has_fraction) > 0 and has_fraction[0]:
            group_fraction = ""
            for group in WordsToInt.__fraction_re__.findall(updated_words):
                fraction_match = WordsToInt.__fraction_re__.match(group[0])
            
                if group[1] in WordsToInt.__fraction__:
                    tens_and_ones = group[0]
                    
                    if group[0] in WordsToInt.__fraction__:
                        return "1/" + str(WordsToInt.__fraction__[group[0]])
                    
                    if tens_and_ones not in WordsToInt.__ones__.keys():
                        split_ones = tens_and_ones.split()
                        tens_and_ones = split_ones[0]
                
                    if tens_and_ones in WordsToInt.__ones__.keys():
                        group_fraction = str(WordsToInt.__ones__[tens_and_ones]) + "/" + str(WordsToInt.__fraction__[group[1]])
                
            return group_fraction
            
        # Para números enteros
        for group in WordsToInt.__groups_re__.findall(updated_words):
            # Determina la posición de este grupo de números
            # dentro del número entero.
            # Se asume que el índice de grupo es el grupo first/ones
            # hasta que se determine que es un grupo superior.
            group_multiplier = 1
            group_num = 0
            
             # Determina el valor de este grupo de números
            if group[1] in WordsToInt.__groups__:
                group_multiplier = WordsToInt.__groups__[group[1]]
           
            # Crea una variable para guardar lo que queda cuando
            # se eliminan las "centenas" (es decir, los valores de las decenas y las unidades)
            hundreds_match = WordsToInt.__hundreds_re__.match(group[0])
            
            tens_and_ones = None
            
            # Se verifica si existe algun digito que coincida con un patrón de "hundreds extra".
            hundreds_match1 = WordsToInt.__hundreds_extra__.match(group[0])
            match_hundreds_extra = hundreds_match1.group(1) in WordsToInt.__hundreds__.keys()
            
            # En caso de que así sea:
            if hundreds_match1 is not None and hundreds_match1.group(1) is not None and match_hundreds_extra:                           
                # Se toma el valor del dígito
                group_num = WordsToInt.__hundreds__[hundreds_match1.group(1)]
                # Se guarda el valor posicional de las decenas y las unidades.
                tens_and_ones = hundreds_match1.group(2)
                       
            # Si hay una cadena en este grupo que coincida con el patrón 'n cien'
            elif hundreds_match is not None and hundreds_match.group(1) is not None:
                # Multiplica el valor 'n' por 100 e incrementa el valor de este grupo
                group_num = group_num +                             (WordsToInt.__ones__[hundreds_match.group(1)] * 100)
                # Se guarda el valor posicional de las decenas y las unidades.
                tens_and_ones = hundreds_match.group(2)
            else:
            # Si no hubiera ninguna cadena que coincidiera con el patrón 'n cien',
            # supone que toda la cadena contiene solo decenas y unidades
            # como valores posicionales.
                tens_and_ones = group[0]
            # Si la cadena de 'decenas y unidades' está vacía, se pasa al siguiente grupo
            if tens_and_ones is None:
                # Incrementa el número total con el número de grupo actual * su multiplicador
                num = num + (group_num * group_multiplier)
                continue
           # Busca las decenas y las unidades 
            tn1_match = WordsToInt.__tens_and_ones_re__.match(tens_and_ones)
            # Si el patrón coincide, hay un valor posicional de 'decenas'
            if tn1_match is not None:
                # Agrega las decenas
                group_num = group_num + WordsToInt.__tens__[tn1_match.group(1)]
                 # Agrega las unidades
                if tn1_match.group(2) is not None:
                    group_num = group_num + WordsToInt.__ones__[tn1_match.group(2)] 
            else:
            # Asume que las 'decenas y unidades' en realidad solo contenían las unidade.
                if tens_and_ones not in WordsToInt.__ones__.keys():
                    split_ones = tens_and_ones.split()
                    tens_and_ones = split_ones[0]
            
            if tens_and_ones in WordsToInt.__ones__.keys():
                group_num = group_num + WordsToInt.__ones__[tens_and_ones]
                
            # Incrementa el número total con el número de grupo actual * su multiplicador
            num = num + (group_num * group_multiplier)
        return num   


"""
Se obtienen los vecinos anteriores y posteriores de una palabra,
de acuerdo a una distancia dada.
"""
def wsd_caracteristicas_colocacion(context, instance, pos, dist=2, punt = []): #TODO CAMBIADO
    features = {}
    con = context
    # la coma esta antes
    punt_prev = True if pos - 1 in punt else None 
    #la coma esta despues
    punt_next = True if pos in punt else None

    # Las palabras serán almacenadas de acuerdo a su posición.
    prev_words = []
    next_words = []

    # A partir de una posición dada, se obtienen las palabras previas requeridas
    # dependiendo la distancia.
    if not punt_prev:
        for i in range(max(0, pos-dist), pos):
            prev_words.append(con[i])
        features["previous"] = (' '.join(prev_words))
    else:
        features["previous"] = ('')

     # A partir de una posición dada, se obtienen las palabras posteriores requeridas
    # dependiendo la distancia.
    if not punt_next:
        for i in range(pos+1, min(pos+dist+1, len(con))):
            next_words.append(con[i])
        features['next'] = (' '.join(next_words))
    else: 
        features['next'] = ('')

      
    return features


"""
Busca los ingredientes
"""
# Se obtienen los vecinos de las palabras conocidas como ingredientes.
def get_ngrams_ingredients(tokenized_words, context, ingredients, dist= 5):
    ngrams_ingredients = []    
    complements = []
    tokenized_ingredients = tokenized_words.copy()
    
    punct = []

    for items in tokenized_words:
        idx = items[0]
        text = items[1]
        data_type = items[6]
        
        for ingredient in ingredients:
            complements = []
            
            if ingredient == text and data_type != "complement":
                # Referencia de que el ingrediente ha sido encontrado
                tokenized_words[idx][6] = "ingredient"
              
                # Se busca al complemento en palabras NEXT, y si lo encuentra, ya no se busca el otro ingrediente.                
                next_word_idx  = idx + 1
                
                next_word_data = tokenized_words[next_word_idx]
                next_word_text =  next_word_data[1]
                next_word_tag  = next_word_data[3]
                
                #validaciones para determinar donde agregar ","
                #determinamos el genero de la palabra
                if tokenized_words[idx][8] != tokenized_words[next_word_idx][8] and len(tokenized_words[next_word_idx][8]) > 0:
                    punct.append(idx)
                
                #determinamos si hay 2 ingredientes seguidos
                if tokenized_words[idx - 1][6] == "ingredient" and tokenized_words[idx][6] == "ingredient" :
                    punct.append(idx - 1)
                 
                wsd_words = wsd_caracteristicas_colocacion(context, ingredient, idx, dist)
                
                # Se analiza si existe una adposición o pronombre después del ingrediente
                if next_word_tag == "ADP":                    
                    # Referencia de que una adposición ha sido encontrada
                    tokenized_words[next_word_idx][6] = "complement"
                    
                    complements.append(next_word_text)
                    
                    # Se buscan pronombres despúes de la adposición
                    for idx in range(next_word_idx + 1, len(tokenized_words)):
                        found_word = tokenized_words[idx]
                        noun_word = found_word[1]
                        noun_tag = found_word[3]
                        
                        if noun_tag == "NOUN":
                            tokenized_words[next_word_idx + 1][6] = "complement"
                            complements.append(noun_word)
                        elif noun_tag != "NOUN":
                              break
                    
                    if len(complements) == 1:
                        complements = []
                    
                ingredient_data = { 
                    text:
                        {
                            "ngrams": wsd_words,
                            "ing_idx": idx,
                            "complements": complements 
                        }
                }
                
                ngrams_ingredients.append(ingredient_data)

    #actualizamos los id de los ingredientes en el ngrams_ingredients para que coincidan los valores
    if len(punct) > 0:

        for indx, ng_ing in enumerate(ngrams_ingredients):
            key, value = next(iter(ng_ing.items()))

            if value["ing_idx"] in punct:
                ngrams_ingredients[indx][key]["ing_idx"] = value["ing_idx"] + punct.index(value["ing_idx"]) + 1

                
    return  ngrams_ingredients, tokenized_ingredients, punct


"""
Busca las cantidades
"""
# Se obtienen los vecinos de las palabras con números.
def get_ngrams_quantity(tokenized_words, context, dist= 4):
    ngrams_numbers = []

    for items in tokenized_words:
        idx = items[0]
        text = items[1]
        lemma = items[2]
        tag = items[3]
    
        # Se obtienen solo los elementos que se encuentran después de un número
        if tag == "NUM" :#or lemma == "uno":
            number_data = { 
                text : 
                    { 
                        "ngrams": wsd_caracteristicas_colocacion(context, text, idx, dist=4),
                        "num_idx": idx 
                    } 
            }
            
            ngrams_numbers.append(number_data)
    
    return ngrams_numbers


"""
Busca las medidas
"""
# Se obtienen los vecinos de las palabras con medidas.
def get_ngrams_measures(tokenized_words, context, measures_set):
    ngrams_measures = []

    for items in tokenized_words:
        idx = items[0]
        text = items[1]
    
        for measure in measures_set:
            if measure == text:
                measure_data = {
                    text: 
                    {
                        "ngrams": wsd_caracteristicas_colocacion(context, measure, idx, dist=4),
                        "measure_idx": idx 
                    }
                }
    
                ngrams_measures.append(measure_data)

    return ngrams_measures


"""
Se obtienen los ingredientes con sus medidas correspondientes.
"""
def get_ingredients_with_measures(tokenized_words, ngrams_measures, ingredients, wtn):
    ingredients_with_measures = {}
    
    print("Procesando ingredientes con medidas...")
    
    for ngrams in ngrams_measures:
        for measure, measure_data in ngrams.items():
            measure_ngrams = measure_data['ngrams']
            measure_idx = measure_data['measure_idx']
        
            prev_words = measure_ngrams["previous"]
            next_words = measure_ngrams["next"]
  
            text = prev_words + " " + next_words
    
            integer = wtn.parse(text)
           
            # Se buscan los ingredients en los vecinos
            for idx, word in enumerate(next_words.split()):
                found = False 
                current_idx_word = measure_idx + (idx + 1)
            
                #  No itera más si hay una "y" y despúes de la "y" existe un pronombre
                if word == "y" and tokenized_words[current_idx_word + 1][3] == "NOUN":
                    break
            
                for ingredient in ingredients:
                    if ingredient not in ingredients_with_measures and ingredient == word and integer != 0:
                        ingredients_with_measures[ingredient] = [ integer, measure, current_idx_word] 
                        found = True # no busca en los vecinos despúes de haber encontrado el ingrediente
                        break
                if found:
                    break
                
    print("Ingredientes con medidas procesados")
    
    return ingredients_with_measures


"""
Se obtienen los ingredientes con sus medidas irregulas correspondientes.
"""
def get_ingredients_with_irregular_measures(irregular_measures_set, ngrams_ingredients):
    ingredients_with_irregular_measures = {}
    
    print("Procesando ingredientes con medidas irregulares...")
    
    measure_list = irregular_measures_set
   
    for ngrams in ngrams_ingredients:
        for ingredient, ingredient_data in ngrams.items():
            ngrams = ingredient_data['ngrams']
            ing_idx = ingredient_data['ing_idx']
        
            prev_words = ngrams["previous"].split()
            
            last_prev_word = prev_words[-1]
            
            if last_prev_word == "de": #TODO optimizar
                del prev_words[-1]
                last_prev_word = prev_words[-1]
        
            if last_prev_word in measure_list:
                ingredients_with_irregular_measures[ingredient] = [ "", last_prev_word, ing_idx] 
    
    print("Ingredientes con medidas procesados")
    
    return ingredients_with_irregular_measures


"""
Busca los ingredientes con sus cantidades correspondientes,
de la lista de n_grams_ingredients.
"""
def find_ingredients_with_quantity(ngrams_ingredients, tokenized_words, ingredients_with_measures, wtn):
    ingredients_with_quantity = []

    print("Procesando ingredientes con cantidad...")
    
    # un platano y medio
    for ngrams in ngrams_ingredients:
        complet_ingredient = []
    
        for ingredient, ingredient_data in ngrams.items():
            ngrams = ingredient_data['ngrams']
            ing_idx = ingredient_data['ing_idx']
    
            prev_words = ngrams["previous"]
            next_words = ngrams["next"]
   
            text = prev_words + " " + next_words #TODO 
            number = tokenized_words[ing_idx][9]
            
            invalid = False
           
            if wtn.parse(prev_words) != 0:
                spl = prev_words.split()  
                for i, word in enumerate(spl):
                    idx = ing_idx - i
                    if idx == ing_idx:
                        continue
                    searched_word = tokenized_words[ing_idx - i]
                    if searched_word[1] == "minutos":
                        invalid = True
                        break
                    
                if invalid:
                    break
                    
                    
            integer = wtn.parse(text)
        
        # Se comprueba si el elemento ya existe en la lista "ingredients_with_measures" o si no contiene una cantidad
            existing_idx = [im[2] for im in ingredients_with_measures.values() if im[2] == ing_idx]
        
            if len(existing_idx) == 1:
                break
           
            if 'Plur' in number and integer == 1 :
                found_item = [ ingredient, "", "", ing_idx ]
            
            elif integer != 0:
                
                found_item = [ ingredient, integer, "", ing_idx]
            else:
                found_item = [ ingredient, "", "", ing_idx ]
        
            if found_item not in ingredients_with_quantity:
                ingredients_with_quantity.append(found_item)
     
    print("Ingredientes con cantidad procesados")   
    return ingredients_with_quantity


"""
Encuentra solo ingredientes sin informaciones extras.
"""
def find_only_ingredients(ingredients_with_quantity):
    only_ingredients = []

    for iq in ingredients_with_quantity: 
        ing_quantity = iq[1]
        if ing_quantity == '':
            only_ingredients.append(iq)
    return only_ingredients



"""
Une los ingredientes con todas sus informaciones encontradas.
"""
def merge_ingredients_measures_quantity(ingredients_with_measures, ingredients_with_irregular_measures, ingredients_with_quantity, only_ingredients):
    final_ingredients = {}
    
    # Agregar ingredientes con medidas y cantidades
    for im in ingredients_with_measures.items():
        ingredient_m = im[0]
        quantity_m = im[1][0]
        measure_m = im[1][1]
        index_m = im[1][2]
    
        for iq in ingredients_with_quantity:
            ingredient_q = iq[0]
            ing_quantity = iq[1]
        
            # Ingredientes con cantidad y medidas
            if ingredient_m == ingredient_q: 
                final_ingredients[ingredient_m] = [ quantity_m, measure_m, index_m ] #optimizar
           
    # Agregar ingredientes con medidas irregulares
    for iim in ingredients_with_irregular_measures.items():
        ingredient_iim = iim[0]
     
        if ingredient_iim in final_ingredients:
            continue
             
        final_ingredients[ingredient_iim] = iim[1]
        
        
    # Agregar solo ingredientes con cantidades
    for iq in ingredients_with_quantity:
        ingredient_q = iq[0]
        quantity_q = iq[1]
    
        if ingredient_q in final_ingredients or quantity_q == '':
            continue
            
        iq_copied = iq.copy()
        iq_copied.remove(ingredient_q)
        
        final_ingredients[ingredient_q] = iq_copied
    
    # Agregar solo ingredientes
    for oi in only_ingredients:
        only_ing = oi[0]
    
        if only_ing not in final_ingredients:
            oi_copied = oi.copy()
            oi_copied.remove(only_ing)
            final_ingredients[only_ing] = oi_copied 

    # Se ordenan por index en el texto
    final_ingredients = dict(sorted(final_ingredients.items(), key=lambda item: item[1][2]))
    return final_ingredients


"""
Obtiene adjetivos de los ingredientes
""" 
def get_adjectives(tokenized_words, final_ingredients):
    final_ingredients_adj = {}

    for v_ingredient in final_ingredients.values():
        adj = []
        v_ingredient_idx = v_ingredient[2]
    
        ingredient = tokenized_words[v_ingredient_idx][1]
    
        for t_word in tokenized_words:
            t_word_idx = t_word[0]
            t_word_word = t_word[1]
            t_word_tag = t_word[3]
            t_word_det = t_word[4]
    
            if t_word_idx == v_ingredient_idx:
                for idx in range(v_ingredient_idx + 1, len(tokenized_words)): # cambiar a infinito
                    searched_adj = tokenized_words[idx]
                    adj_word = searched_adj[1]
                    adj_tag = searched_adj[3]
                    adj_dep = searched_adj[5]
                       
                    if adj_dep == "amod" or adj_dep == "nmod" or adj_dep == "appos":
                        adj.append(adj_word)
                    else:
                        break
                    
        final_ingredients_adj[ingredient] = adj
    
    return final_ingredients_adj


"""
Obtiene complementos de los ingredientes
""" 
def get_complements(ngrams_ingredients, final_ingredients, final_ingredients_adj):
    ingredients_complement = {}

    for v_ingredient in final_ingredients:
        complements_data = []
    
        v_ingredient_idx = final_ingredients[v_ingredient][2]
        
        for ngrams in ngrams_ingredients:
            for ingredient, ingredient_data in ngrams.items():
                complements = ingredient_data['complements']
                ing_idx = ingredient_data['ing_idx']
            
                if v_ingredient_idx == ing_idx and len(complements) > 0:
                    ingredients_complement[ingredient] = complements
                
        final_ingredients_adj.update(ingredients_complement)
        
    return final_ingredients_adj


"""
Obtiene los ingredientes con toda su información correspondiente como diccionario.
"""
def merge_ingredients_data(final_ingredients, final_ingredients_adj):
    total_ingredients = {}
    
    for index, ingredient in enumerate(final_ingredients):
        q_data_original = final_ingredients[ingredient].copy()
        q_data = q_data_original[:-1]
    
        if ingredient not in final_ingredients_adj:
            total_ingredients[ingredient] = { "quantity": q_data , "description": [] }
            continue
        
        adj_data = final_ingredients_adj[ingredient]
    
        total_ingredients[ingredient] = { "quantity": q_data , "description": adj_data }
    
    return total_ingredients





"""
Convierte los datos de los ingredientes a texto.
"""
def ingredients_data_to_string(data_ingredients):
    ingredients_to_text = ""
    
    for t_ingre in data_ingredients:
        cantidad = data_ingredients[t_ingre]['quantity'][0]
        medida = data_ingredients[t_ingre]['quantity'][1]
        descripcion = ' '.join(data_ingredients[t_ingre]['description'])
   
        if cantidad and medida:
            medida += " de" 
        
        ingredient_array = [str(cantidad), medida, t_ingre, descripcion]
        ingredient_string = " ".join(ingredient_array)
        ingredient_string = re.sub(' +',' ', ingredient_string)
        
        ingredients_to_text += "\n" + ingredient_string
        
    return ingredients_to_text




"""
Se obtienen los ingredientes de un texto.
"""
def get_ingredients_from_text(parsed_text):
    tokenized_words = get_tokenized_words(parsed_text)

    words_text = get_word_text(tokenized_words)
    
    # Se obtienen los datos de los datasets
    list_ingredients = ingredients()
    print(list_ingredients)
    measures_set = get_measures_from_file('medidas.json')
    
    # Medidas que nunca tienen cantidades
    irregular_measures_set = parse_json_file('medidas irregulares.json')
    
    # Se inicializa la clase
    wtn = WordsToInt()
    
    # Se obtienen los vecinos de los datos necesarios (ingredientes, cantidades y medidas)
    ngrams_ingredients, tokenized_ingredients, position_punct = get_ngrams_ingredients(tokenized_words, words_text, list_ingredients)

    tokenized_words = insert_punct(tokenized_words, position_punct)
        
    ngrams_numbers = get_ngrams_quantity(tokenized_words, words_text)
    ngrams_measures = get_ngrams_measures(tokenized_words, words_text, measures_set)
    
    # Se obtienen los datos de los ingredientes encontrados
    ingredients_with_measures = get_ingredients_with_measures(tokenized_words, ngrams_measures, list_ingredients, wtn)
    ingredients_with_irregular_measures = get_ingredients_with_irregular_measures(irregular_measures_set, ngrams_ingredients)
    ingredients_with_quantity = find_ingredients_with_quantity(ngrams_ingredients, tokenized_words, ingredients_with_measures, wtn)

    only_ingredients = find_only_ingredients(ingredients_with_quantity)
     
    # Se obtienen todos los ingredientes encontrados
    final_ingredients = merge_ingredients_measures_quantity(ingredients_with_measures, ingredients_with_irregular_measures, ingredients_with_quantity, only_ingredients)
   
    # Se obtienen los adjetivos y complementos
    final_ingredients_adj = get_adjectives(tokenized_words, final_ingredients)
    final_ingredients_complements = get_complements(ngrams_ingredients, final_ingredients, final_ingredients_adj)
    
    # Se unen las informaciones de los ingredientes encontrados
    return merge_ingredients_data(final_ingredients, final_ingredients_complements)


"""
Mide el grado de similitud entre dos palabras.
"""
def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


"""
Se realiza un pre-procesamiento de ingredientes, para eliminar los elementos repetidos o parecidos.
""" 
def preprocess_ingredients(parsed_ingredients):  
    ingredients_text = " ".join(parsed_ingredients)

    copy_parsed_ingredients = parsed_ingredients.copy()

    # Se verificar los elementos similares.
    # El elemento con índice mayor será eliminado
    # si tiene similaridad de 80%.
    for i, initial_ingred in enumerate(parsed_ingredients):
        for io, other_ingred in enumerate(parsed_ingredients):
            if i >= io:
                continue
    
            similarity = jaccard_similarity(initial_ingred, other_ingred)
            if similarity > 0.80:
                del copy_parsed_ingredients[other_ingred]
    
    return ingredients_data_to_string(copy_parsed_ingredients)


def extract_ingredients():
    textfile = os.getcwd() + "/Converted_results/" + "Converted_audio.txt"
    last_ingredients = ""

    print("::Se estan extrayendo los ingredientes...")

    try:
        with open(textfile) as file:
            fileContent = file.read()
            file.close()
    except FileNotFoundError:
         print(f'The file {textfile} does not exist')
    else:
        parsed_text = parse_text(fileContent)
        from_description = get_text_from_description(parsed_text)
    
        if len(from_description) == 0:
            parsed_ingredients = get_ingredients_from_text(parsed_text)

            last_ingredients = preprocess_ingredients(parsed_ingredients)
        else:
            last_ingredients = " ".join(from_description)
    
    print(last_ingredients)
    return last_ingredients

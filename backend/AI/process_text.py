#!/usr/bin/env python
# coding: utf-8

import spacy
from spacy.tokens import Token
import re
import language_tool_python


from pattern.es import pluralize
from pattern.es import singularize
from AI.process_ingredients import ingredients

#declaracion de las librerias de NPL
nlp = spacy.load("es_core_news_lg")
nlp_trf = spacy.load("es_dep_news_trf")
tool = language_tool_python.LanguageTool('es')



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

# Verificamos si la palabra es un ingrediente
def ingredient(token):
    ingr = ingredients()
    return token.text.lower() in ingr is not False

#verificamos si el token es un simbolo
def symbol(token):
    # Expresión regular que busca cualquier caracter que no sea una letra, número o espacio en blanco
    patron = r'[^a-zA-Z1-9ñÑáéíóúÁÉÍÓÚüÜ\d\s/\d.]'
    # Buscamos el patrón en el texto
    res = re.search(patron, token.text)
    # Si se encuentra algún símbolo devuelve True
    return res is not False


#verificamos la gramatica d ela sentencia
def grammar_validate(sentence):
    matches = tool.check(sentence)
    if len(matches) > 0:
        #La oración tiene errores sintácticos.
        return False
    else:
        #La oración es gramaticalmente correcta.
        return True


#validamos que la palabra sea correcta
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



def Doc(text, type = "lg"):
    #creamos nuestras propiedades personalizadas
    Token.set_extension('is_semantic', getter=semantic, force=True)
    Token.set_extension('is_syntax', getter=syntax, force=True)
    Token.set_extension('is_spanish', getter=spanish_word, force=True)
    Token.set_extension('is_consonant', getter=consonant, force=True)
    Token.set_extension('is_symbol', getter=symbol, force=True)
    Token.set_extension('is_ingredient', getter=ingredient, force=True)
    Token.set_extension('need_punct', default=False, force=True)


    if type == "lg": 
        return nlp(text) 
    else:
        return nlp_trf(text)



def parse_text(text, prev_doc = []):
    parsed_text = []
    
    doc = Doc(text)
    
    for idx, token in enumerate(doc):
        if not token.like_url and not token.like_email:
            description = prev_doc[idx][6] if len(prev_doc) > 0 else ""
            punt = prev_doc[idx][7] if len(prev_doc) > 0 else token._.need_punct
            parsed_text.append([token.text.lower(), token.lemma_, token.pos_, spacy.explain(token.pos_), token.dep_, description, punt, token.morph.get("Gender"), token.morph.get('Number')])

    return parsed_text     


def get_tokenized_words(parsed_text):
    tokenized_words = []
    
    stopwords = [".", ",", "mi", "hola", "mmm", "gracias", "\n", " "]

    no_stopwords = [word for word in parsed_text if word[0] not in stopwords]

    for index, word in enumerate(no_stopwords):
        word.insert(0, index)
        tokenized_words.append(word)
        
    return tokenized_words

"""
Obtiene solo el texto de las palabras
"""
def get_word_text(words):
    return [word[1] for word in words]


"""
Se inserta una "," entre las palabras del texto que corresponda.
"""
def insert_punct(tokenized_words, position):

    
    # invertimos la lista de posiciones para agregar la "," de atras hacia adelante pra no alterar los ids de posiciones recibidos y ubicarlo en el lugar correcto
    reverse_position = sorted(position, reverse=True)

    #recorremos las posiciones y las buscamos en el texto, le sumamos una posicion y agregamos la "," y actualizamos el valor del tetxo de  que requiere punt en True
    for pos in reverse_position:
        tokenized_words[pos][7] = True
        tokenized_words.insert(pos + 1, [pos + 1, ',', ',', 'PUNCT', 'punctuation', 'punct', '', False, [], []])

    print("::tokenized_words", tokenized_words)
    #actualizamos las properties correspondientes a cada palabra
    text = [ token[1] for token in tokenized_words]
    doc = Doc(" ".join(text))
    parsed_text = parse_text(doc, tokenized_words)

    return get_tokenized_words(parsed_text)


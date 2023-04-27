#!/usr/bin/env python
# coding: utf-8


import nltk

# nltk.download()

# Librerías para PNLIngred_Description
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import language_tool_python
from spacy.matcher import Matcher
from spacy.util import filter_spans


# Otras librerías
import os
import shutil
import pandas as pd
from collections import Counter
import json
import re

#import AI.process_text
from AI.process_text import Doc, word_validate, grammar_validate , nlp
from constants.constants import patterns

def extract_procedure(text):
    #textfile = os.getcwd() + "/Converted_results/" + "Converted_audio.txt"

    try:
        # with open(textfile) as file:
        #     fileContent = file.read()
        #     file.close()
   
        tool = language_tool_python.LanguageToolPublicAPI('es-MX')

        #nlp = spacy.load("es_dep_news_lg")

        # instantiate a Matcher instance
        matcher = Matcher(nlp.vocab)
        matcher.add("Verb phrase", patterns)

        doc = Doc(text)

        # call the matcher to find matches
        matches = matcher(doc)
        spans = [doc[start:end] for _, start, end in matches]

        value_list = filter_spans(spans)
        value_list

        tool = language_tool_python.LanguageToolPublicAPI('es-MX')

        procedure_to_string = ""
        procedures = []

        for number, sentence in enumerate(value_list):
            my_mistakes = []
            my_corrections = []

            text = str(sentence)

            matches = tool.check(text)

            for rules in matches:
                if rules.ruleId == 'MORFOLOGIK_RULE_ES':  # no nos importa que reemplace ingredientes
                    continue
                else:
                    my_mistakes.append(
                        text[rules.offset: rules.errorLength + rules.offset])
                    my_corrections.append(rules.replacements[0])

            if len(my_corrections) == 0:
                procedure_to_string += "\n" + str(number + 1) + ".- " + text + "."
                continue

            new_text = text

            #  for word in text.split():
            for i, mistake in enumerate(my_mistakes):
                new_text = new_text.replace(my_mistakes[i], my_corrections[i])

            procedure_to_string = "\n" + str(number + 1) + ".- " + new_text + "."
            procedures.append(procedure_to_string)

        # Crea el archivo de ingredientes
        # with open('recipe procedure.txt', 'w') as f:
        # f.write("PROCEDIMIENTO:\n")
        # f.write(procedure_to_string)

        # f.close()

        return procedures

    except FileNotFoundError:
        #print(f'The file {textfile} does not exist')
        return False

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk

#nltk.download()

# Librerías para PNLIngred_Description
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
#import es_dep_news_trf # https://spacy.io/usage/models
import language_tool_python
from spacy.matcher import Matcher
from spacy.util import filter_spans


# Otras librerías
import os, shutil
import pandas as pd
from collections import Counter
import json
import re

#!python -m spacy download es_dep_news_trf
#conda install -c conda-forge spacy-model-es_dep_news_trf
#!pip install xlrd
#pip install language-tool-python


# In[2]:


#!python -m spacy download es_core_news_sm / es_core_news_lg


# In[7]:


textfile = os.getcwd() + "\\Converted results\\" + "Converted_audio.txt"

try:
    with open(textfile) as file:
        fileContent = file.read()
        file.close()
except FileNotFoundError:
     print(f'The file {textfile} does not exist')


tool = language_tool_python.LanguageToolPublicAPI('es-MX')


# In[10]:


verbs_stop_lemma = ["estar", "tener", "basar"]
nouns_stop_text = ["personas", "vuelta", "manita"]
morph_attributes = {"INTERSECTS": ["VerbForm=Inf"]}

pattern = [
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # agregarle las rajas
           {'POS': 'DET', 'OP': '{0}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}}
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # agregarle las rajas
           {'POS': 'DET', 'OP': '{0,}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'ADP', 'OP': '{0,}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
     #      {'POS': 'PRON', 'OP': '?'},
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # dejar aquí 15 minutos
           {'POS': 'ADV', 'OP': '?'},
           {'POS': 'NUM', 'OP': '?'},
           {'POS': 'NOUN', 'OP': '{1}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}}
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # desvenar estos chilitos guajillos
           {'POS': 'DET', 'OP': '?'},
           {'POS': 'NOUN', 'OP': '{1}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'ADJ', 'OP': '?'},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # poner poquito agua,
           {'POS': 'ADJ', 'OP': '{1}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # poner poquito de aceite,
           {'POS': 'ADV', 'OP': '{1}'},
           {'POS': 'ADP', 'OP': '{1}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # agregarle las rajas
           {'POS': 'DET', 'OP': '{0,}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'DET', 'OP': '?'},
           {'POS': 'NOUN', 'OP': '?', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'CCONJ', 'OP': '{1}'},
           {'POS': 'DET', 'OP': '{0,}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # dejar que hierva bien,
           {'POS': 'SCONJ', 'OP': '{1}'},
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}}, 
           {'POS': 'ADV', 'OP': '{1}'},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # meter en una bolsa de plastico
           {'POS': 'ADP', 'OP': '{1}'},
           {'POS': 'DET', 'OP': '{1}'}, 
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'ADP', 'OP': '{1}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # tapar con un secador
           {'POS': 'ADP', 'OP': '{1}'},
           {'POS': 'DET', 'OP': '{1}'}, 
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
    [
           {'POS': 'VERB', 'OP': '{1}', "LEMMA": {"NOT_IN": verbs_stop_lemma}, "MORPH": morph_attributes}, # poner una taza y media de crema
           {'POS': 'DET', 'OP': '{1}'},    
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
           {'POS': 'CCONJ', 'OP': '{1}'},
           {'POS': 'NUM', 'OP': '{1}'},
           {'POS': 'ADP', 'OP': '{1}'},
           {'POS': 'NOUN', 'OP': '{1,}', "DEP": {"NOT_IN": ["compound"]}, 'TEXT': {"NOT_IN": nouns_stop_text}},
    ],
     
]


# In[11]:


nlp = spacy.load("es_dep_news_trf")

# instantiate a Matcher instance
matcher = Matcher(nlp.vocab)
matcher.add("Verb phrase", pattern)

doc = nlp(fileContent)

# call the matcher to find matches 
matches = matcher(doc)
spans = [doc[start:end] for _, start, end in matches]

value_list = filter_spans(spans)
value_list


# In[12]:


tool = language_tool_python.LanguageToolPublicAPI('es-MX')

procedure_to_string = ""

for number, sentence in enumerate(value_list):
    my_mistakes = []
    my_corrections = []

    text = str(sentence)
    
    matches = tool.check(text)
    
    for rules in matches:      
        if rules.ruleId == 'MORFOLOGIK_RULE_ES': # no nos importa que reemplace ingredientes
            continue
        else:
            my_mistakes.append(text[rules.offset : rules.errorLength + rules.offset])
            my_corrections.append(rules.replacements[0])
            
               
    if len(my_corrections) == 0:
        procedure_to_string += "\n" + str(number + 1) + ".- " + text + "."
        continue
    
    new_text = text
    
  #  for word in text.split():
    for i, mistake in enumerate(my_mistakes):
        new_text = new_text.replace(my_mistakes[i], my_corrections[i])

    procedure_to_string += "\n" + str(number + 1) + ".- " + new_text + "."

print(procedure_to_string)

# In[13]:


# Crea el archivo de ingredientes
with open('recipe procedure.txt', 'w') as f:
    f.write("PROCEDIMIENTO:\n")
    f.write(procedure_to_string)

    f.close()


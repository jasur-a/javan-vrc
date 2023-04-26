#CONSTANTS

verbs_stop_lemma = ["estar", "tener", "basar"]
nouns_stop_text = ["personas", "vuelta", "manita"]
morph_attributes = {"INTERSECTS": ["VerbForm=Inf"]}

patterns = [
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

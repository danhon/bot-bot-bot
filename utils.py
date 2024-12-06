import tracery
from tracery.modifiers import base_english

import json
import os

def generate_post(rules):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    post = grammar.flatten("#origin#")
    return post

def generate_post_short(rules):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    post = grammar.flatten("#origin#")

    while len(post) > 260:
        post = grammar.flatten("#origin#")
        if len(post) < 260:
            break
    return post

def get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON):
    file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

    with open(file_path) as rules_file:
        rules = json.load(rules_file)

    return rules
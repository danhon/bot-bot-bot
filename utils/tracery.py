import os
import logging
import pyjson5
import sys

import tracery
from tracery.modifiers import base_english

# create logger
module_logger = logging.getLogger('bot-bot-bot.utils.tracery')

def generate_posts(rules):
    """Returns a dict containing two Tracery grammars with keys ["long"] and ["short"] when supplied a json Tracaery rules file."""
    post = {}
    
    module_logger.info('Generating a post')
 
    post['long'] = generate_post(rules)
    post["short"] = generate_post_short(rules)

    module_logger.info('Done generating a post')

    # pprint.pp(len(post["short"]))
    # pprint.pp(len(post["long"]))
    
    return post

def generate_post(rules):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    long_post = grammar.flatten("#origin#")

    while len(long_post) > 500:
        long_post = grammar.flatten("#origin#")
    return long_post

def generate_post_short(rules):
    short_post = generate_post(rules)

    while len(short_post) > 260:
        short_post = generate_post(rules)
        if len(short_post) < 260:
            break
    return short_post

def get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON):
    """Returns a json rules object to be used with a Tracery grammar"""
    file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)
 
    module_logger.info('Opening rules file %s.', GRAMMAR_JSON)
 
    try: 
        with open(file_path) as rules_file:
            rules = pyjson5.decode_io(rules_file)

        module_logger.info('Done getting rules.')

    except OSError:
        print("Couldn't open: ", file_path)
        sys.exit()

    return rules

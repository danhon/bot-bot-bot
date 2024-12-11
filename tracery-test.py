import os
import sys
import pyjson5

import tracery
from tracery.modifiers import base_english

# create logger





# def get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON):
#     """Returns a json rules object to be used with a Tracery grammar"""
#     file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)
 
#     module_logger.info('Opening rules file %s.', GRAMMAR_JSON)
 
#     try: 
#         with open(file_path) as rules_file:
#             rules = pyjson5.decode_io(rules_file)

#         module_logger.info('Done getting rules.')

#     except OSError:
#         print("Couldn't open: ", file_path)
#         sys.exit()

#     return rules


# def generate_post(rules):
#     grammar = tracery.Grammar(rules)
#     grammar.add_modifiers(base_english)
#     post = grammar.flatten('#origin#')
#     return post

file_path = os.path.join('grammars/', 'startrek-granddesigns.json')

try: 
    with open(file_path) as rules_file:
        rules = pyjson5.decode_io(rules_file)

    module_logger.info('Done getting rules.')

except OSError:
    print("Couldn't open: ", file_path)
    sys.exit()

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print(grammar.flatten('#origin'))
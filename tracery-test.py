import os
import sys
import pyjson5
import pprint
import tracery
from tracery.modifiers import base_english
import inspect
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

except OSError:
    print("Couldn't open: ", file_path)
    sys.exit()

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)


# pprint.pp(vars(grammar))

# flattened = grammar.flatten('#origin#')
# print(flattened)

#expanded = grammar.expand('#origin#')
# pprint.pp(vars(expanded))
#pprint.pp(vars(expanded))

trace = grammar.create_root('#origin#')
print("this is the trace object)")
pprint.pp(vars(trace))

thing = trace.expand()

print("this is the expanded trace object")
pprint.pp(vars(thing))
# expanded_grammar = grammar.expand('#origin#').grammar

# pprint.pp(vars(expanded_grammar))


# grammar.expand('#origin#')

# thing = grammar.flatten('#origin#')

# # this should be a node
# thing_expanded_node = grammar.expand('#origin#', type=-1)

# pprint.pp(vars(grammar))

# pprint.pp(vars(grammar.flatten('#origin#')))

# trace = grammar.create_root('#origin#')

# print(type(trace))
# print(dir(trace))
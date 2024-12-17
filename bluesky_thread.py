import os
import logging
import json
import pyjson5
from dotenv import load_dotenv
import argparse
import pprint
import sys

from itertools import repeat

# Bot utilities
from utils.bluesky import get_bluesky_instance, post_thread

from utils.tracery import get_rules, generate_bluesky_thread

# Get base rules
rules = get_rules('grammars/','startrek-granddesigns.json')

# update corpora rules
rules.update(get_rules('grammars/corpora','corpora_numbers.json'))

# Update with star trek rules
startrek_rules =  ["corpora_startrek.json", "corpora_startrek_medical.json", "corpora_startrek_names.json", "corpora_startrek_places.json", "corpora_startrek_ships.json"]

for ruleset in startrek_rules:
    print("loaded:", ruleset)
    rules.update(get_rules('grammars/corpora/',ruleset))


# generate a thread of posts based on the ruleset
thread_of_posts = generate_bluesky_thread(rules)

# bluesky client setup
BLUESKY_USERNAME = "me-im-asking.bsky.social"
BLUESKY_PASSWORD = "imeg-xpep-ikc4-nqno"
BLUESKY_CLIENT =  "https://bsky.social"

# BLUESKY_USERNAME = "st-grand-designs.bsky.social"
# BLUESKY_PASSWORD = "pmvr-flgv-lqyv-qvgx"
# BLUESKY_CLIENT =  "https://bsky.social"

client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)

# actually post them
post_thread(thread_of_posts, client)



# for idx, post in enumerate(thread_of_posts):
#     print(idx, len(post.text), post.text)


# def check_for_length(rules):
#     for _ in repeat(None,5):

#         thread_posts = generate_bluesky_thread(rules)

#         for idx, post in enumerate(thread_posts):
#             print(idx, len(post.text))        

#         print(any(len(post.text) < 260 for (post) in thread_posts))
#         print("---")
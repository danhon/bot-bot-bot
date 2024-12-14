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
from utils.bluesky import get_bluesky_instance, bluesky_faceted_post
from utils.bluesky import bluesky_reply, Post_in_Thread
from atproto import models

from utils.tracery import get_rules, generate_posts, generate_normal_post, generate_bluesky_thread

# Get base rules
rules = get_rules('grammars/','startrek-granddesigns.json')

# update corpora rules
rules.update(get_rules('grammars/corpora','corpora_numbers.json'))

# Update with star trek rules
startrek_rules =  ["corpora_startrek.json", "corpora_startrek_medical.json", "corpora_startrek_names.json", "corpora_startrek_places.json", "corpora_startrek_ships.json"]

for ruleset in startrek_rules:
    print("loaded:", ruleset)
    rules.update(get_rules('grammars/corpora/startrek/',ruleset))

thread_of_posts = generate_bluesky_thread(rules)

# BLUESKY_USERNAME = "me-im-asking.bsky.social"
# BLUESKY_PASSWORD = "imeg-xpep-ikc4-nqno"
# BLUESKY_CLIENT =  "https://bsky.social"

BLUESKY_USERNAME = "st-grand-designs.bsky.social"
BLUESKY_PASSWORD = "pmvr-flgv-lqyv-qvgx"
BLUESKY_CLIENT =  "https://bsky.social"

client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)

def post_thread(thread_of_posts):

    for idx, post in enumerate(thread_of_posts):
        print(idx, len(post.text), post.text)

        
        if idx == 0:
            this_post = client.send_post(post.text)
            root_post = this_post

            post.root_post = root_post
            post.post = this_post

        
        else: 
            previous_post = thread_of_posts[idx-1]

            root_post = previous_post.root_post
            # print(root_post)
            parent_post = previous_post.post

            parent = models.create_strong_ref(parent_post)
            root = models.create_strong_ref(root_post)
                    
            this_post = client.send_post(
                text = post.text,
                reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
            )

            post.root_post = root_post
            post.parent_post = parent_post
            post.post = this_post
            print (idx, post.parent_post)


# actually post them
post_thread(thread_of_posts)



# for idx, post in enumerate(thread_of_posts):
#     print(idx, len(post.text), post.text)


# def check_for_length(rules):
#     for _ in repeat(None,5):

#         thread_posts = generate_bluesky_thread(rules)

#         for idx, post in enumerate(thread_posts):
#             print(idx, len(post.text))        

#         print(any(len(post.text) < 260 for (post) in thread_posts))
#         print("---")
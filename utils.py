import os
from dotenv import load_dotenv
import pprint
import json
import re

import tracery
from tracery.modifiers import base_english

from mastodon import Mastodon
from atproto import Client, client_utils

# def generate_posts(rules):
#     """Returns a dict containing two Tracery grammars with keys ["long"] and ["short"] when supplied a json Tracaery rules file."""
#     post = {}
    
#     post["long"] = generate_post(rules)
#     post["short"] = generate_post_short(rules)
    
#     # pprint.pp(len(post["short"]))
#     # pprint.pp(len(post["long"]))
    
#     return post

# def generate_post(rules):
#     grammar = tracery.Grammar(rules)
#     grammar.add_modifiers(base_english)
#     long_post = grammar.flatten("#origin#")
#     return long_post

# def generate_post_short(rules):
#     short_post = generate_post(rules)

#     while len(short_post) > 260:
#         short_post = generate_post(rules)
#         if len(short_post) < 260:
#             break
#     return short_post

# def get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON):
#     """Returns a json rules object to be used with a Tracery grammar"""
#     file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

#     with open(file_path) as rules_file:
#         rules = json.load(rules_file)
#     return rules

# def mastodon_client():
#     """Returns a usable Mastodon instance based on the environment variables MASTODON_TOKEN and MASTODON_BASE_URL"""
#     environment = envs()
#     MASTODON_TOKEN = environment["MASTODON_TOKEN"]
#     MASTODON_BASE_URL = environment["MASTODON_BASE_URL"]

#     mastodon_instance = Mastodon(
#         access_token=MASTODON_TOKEN,
#         api_base_url=MASTODON_BASE_URL
#     )

#     return mastodon_instance

def bluesky_instance():
    """Returns a Bluesky client based on the environment variables BLUESKY_USERNAME and BLUESKY_PASSWORD. Assumes that your client/pds is at bsky.social"""
    environment = envs()
    BLUESKY_USERNAME = environment["BLUESKY_USERNAME"]
    BLUESKY_PASSWORD = environment["BLUESKY_PASSWORD"]

    client = Client("https://bsky.social")

    client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
    # print("generated a client")
    return client

def bluesky_faceted_post(post):
    """Returns a textbuilder object with tags"""
    post_without_tags = post.split('#')[0]

    text_builder = client_utils.TextBuilder()
    text_builder.text(post_without_tags)

    # parse the hashtags
    hashtags = re.findall(r"#\w+", post)
    # pprint.pp(hashtags)
 
    # add tags 
    for tag in hashtags:
        # Add each hashtag as a tag facet
        text_builder.tag(tag + " ", tag.split('#')[1])

    return text_builder

def envs():
    load_dotenv()
    return os.environ
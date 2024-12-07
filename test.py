import os
import pprint
import json
from dotenv import load_dotenv
from utils.tracery import get_rules, generate_posts
from utils.mastodon_client import mastodon_client 
from utils.bluesky import bluesky_instance, bluesky_faceted_post

load_dotenv()

# set grammars directory and file
GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
GRAMMAR_JSON = "starfleetjobs.json"

rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)


# Load and set environment variables
load_dotenv()

# set grammars directory and file
GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
GRAMMAR_JSON = "starfleetjobs.json"

# make a mastodon client and then post
def post_to_mastodon(post):
    mastodon_instance = mastodon_client()
    mastodon_instance.status_post(post["long"])

# make a bluesky client 
def post_to_bluesky(post):
    bluesky_client = bluesky_instance()
    bluesky_post = bluesky_faceted_post(post["short"])
    bluesky_client.post(bluesky_post)

# get our tracery rules
rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

# generate our posts dict containing a short post and a long post
post = generate_posts(rules)

# send that post to um a posting thing
post_to_mastodon(post)
post_to_bluesky(post)
from mastodon import Mastodon
import os
import tracery
from tracery.modifiers import base_english
import pprint
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create an instance of the Mastodon class

MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
MASTODON_BASE_URL = os.getenv("MASTODON_BASE_URL")

mastodon = Mastodon(
    access_token=MASTODON_TOKEN,
    api_base_url=MASTODON_BASE_URL
)

# set grammars directory and file
GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
GRAMMAR_JSON = "starfleetjobs.json"

# load the tracery grammar
file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

# pprint.pprint(file_path)
with open(file_path) as rules_file:
    rules = json.load(rules_file)
    # now we're ready to go

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
post = grammar.flatten("#origin#")

# Post a new status update
mastodon.status_post(post)
pprint.pp(post)

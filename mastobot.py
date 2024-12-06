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

pprint.pp(MASTODON_TOKEN)
pprint.pp(MASTODON_BASE_URL)

mastodon = Mastodon(
    access_token=MASTODON_TOKEN,
    api_base_url=MASTODON_BASE_URL
)

# Load bot json
json_rules = "starfleetjobs.json"
sub_dir = "dev/bot-bot-bot/grammars/"

file_path = os.path.expanduser(f"~/{sub_dir}/{json_rules}")

pprint.pprint(file_path)
with open(file_path) as rules_file:
    rules = json.load(rules_file)

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
post = grammar.flatten("#origin#")

# Post a new status update
mastodon.status_post(post)
pprint.pp(post)

from mastodon import Mastodon
import os
import tracery
from tracery.modifiers import base_english
import pprint
import json

# Create an instance of the Mastodon class
mastodon = Mastodon(
    access_token='mP_PoDHqE0buKi6yND9xh0qBzPkN8v0AeJZQY9Rv9uY',
    api_base_url='https://botsin.space/'
)

# Load bot json
json_rules = "starfleetjobs.json"
sub_dir = "dev/starfleet-bot"

file_path = os.path.expanduser(f"~/{sub_dir}/{json_rules}")

pprint.pprint(file_path)
with open(file_path) as rules_file:
    rules = json.load(rules_file)

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
post = grammar.flatten("#origin#")

# Post a new status update
mastodon.status_post(post)

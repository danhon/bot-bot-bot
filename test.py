import os
import pprint
import json
from dotenv import load_dotenv
from utils import generate_post, generate_post_short, get_rules


# Load environment variables
load_dotenv()

# set grammars directory and file
GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
GRAMMAR_JSON = "starfleetjobs.json"

rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)
post = generate_post_short(rules)

pprint.pp(post)
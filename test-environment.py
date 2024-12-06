from dotenv import load_dotenv
import pprint
import os
import json

# Load environment variables

load_dotenv()

# set grammars directory and file
GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
GRAMMAR_JSON = "starfleetjobs.json"

# load the tracery grammar
file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

# pprint.pprint(file_path)
with open(file_path) as rules_file:
    rules = json.load(rules_file)
    # now we're ready to go
    
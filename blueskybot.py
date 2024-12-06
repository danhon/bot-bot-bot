import os
import pprint
import tracery
from tracery.modifiers import base_english
import json
import re
from atproto import Client, client_utils
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bluesky credentials
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

# Create a Bluesky client
client = Client("https://bsky.social")



# Load bot json
json_rules = "starfleetjobs.json"
sub_dir = "dev/bot-bot-bot/grammars"

file_path = os.path.expanduser(f"~/{sub_dir}/{json_rules}")

pprint.pprint(file_path)
with open(file_path) as rules_file:
    rules = json.load(rules_file)

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
post = grammar.flatten("#origin#")

while len(post) > 260:
    post = grammar.flatten("#origin#")
    if len(post) < 260:
            break
    
print(post)
print(len(post))

post_without_tags = post.split('#')[0]

print(post_without_tags)



def main():

    client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
    
    text_builder = client_utils.TextBuilder()

    text_builder.text(post_without_tags)


    # parse the hashtags
    hashtags = re.findall(r"#\w+", post)
    pprint.pp(hashtags)
 
    # add tags? 
    for tag in hashtags:
        # Add each hashtag as a tag facet
        text_builder.tag(tag + " ", tag.split('#')[1])

    client.post(text_builder)

    
    # client.post("🙂")

if __name__ == "__main__":
    main()

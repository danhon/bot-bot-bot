import os
import logging
import pprint
import json
from dotenv import load_dotenv

from utils.tracery import get_rules, generate_posts
from utils.mastodon import mastodon_client 
from utils.bluesky import bluesky_instance, bluesky_faceted_post

# set up the logger
logger = logging.getLogger('bot-bot-bot')
logger.setLevel(logging.DEBUG)

# Console logging handler set to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# File logging handler set to info
fh = logging.FileHandler('bot-bot-bot.log')
fh.setLevel(logging.INFO)

# Set the formatter for root
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add console and file handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

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

def main():
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='bot-bot-bot.log', level=logging.DEBUG)

    logger.info('Started')
    logger.debug('Debug message')
    logger.info('Finished')

    print(GRAMMARS_DIRECTORY)
    print(GRAMMAR_JSON)
    # get our tracery rules
    rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

    # generate our posts dict containing a short post and a long post
    post = generate_posts(rules)

    # send that post to um a posting thing
    # post_to_mastodon(post)
    # post_to_bluesky(post)

if __name__ == '__main__':
    main()


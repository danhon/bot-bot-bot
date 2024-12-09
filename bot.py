import os
import logging
import pprint
import json
from dotenv import load_dotenv

from utils.tracery import get_rules, generate_posts
from utils.mastodon import mastodon_client, mastodon_client_multiple
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
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s: %(funcName)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
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

    # Set the grammars directory from os environment
    GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
    logger.info('Using grammars directory "%s"', GRAMMARS_DIRECTORY)

    
    # get the bots 
    logger.info('Opening bots.json')
    
    with open('bots.json') as bots_json:
        bots = json.load(bots_json)
    
    logger.info("Found %s bots", len(bots))


    for idx, bot in enumerate(bots):
        logger.info('Starting bot %s of %s: %s', idx+1, len(bots), bot['name'])


        # Get the grammars
        GRAMMAR_JSON = bot['grammar_json']
        logger.debug("Bot '%s' using grammar %s", bot['name'], bot['grammar_json'])

        logger.info('Getting rules for %s...', bot['name'])
        rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

        # Generate a post
        logger.info('Starting post generation for %s...', bot['name'])
        posts = generate_posts(rules)
        logger.info('Finished post generation for %s.', bot['name'])

        # Getting services
        logger.info('Getting services for %s.', bot['name'])
        for idx, service in enumerate(bot['service']):

            logger.debug("Service %s of %s for %s: %s", idx+1, len(bot['service']), bot['name'], service['service_type'])
        
            match service['service_type']:
                
                case 'mastodon':
                    logger.info("Found a mastodon service")
                    MASTODON_ACCESS_TOKEN = service['access_token']
                    MASTODON_BASE_URL = service['base_url']
                    logger.debug("Mastodon token %s, base URL %s", MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                    logger.info("Set up mastodon service")

                    post = posts['long']

                    mastodon_instance = mastodon_client_multiple(MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                    
                    # mastodon_instance.status_post(post)
                    logger.info('Posted to Mastodon: %s', post)


                case 'bluesky':
                    logger.info("Found a bluesky service")
                    BLUESKY_USERNAME = service['username']
                    BLUESKY_PASSWORD = service['password']
                    BLUESKY_CLIENT = service['client']
                    logger.debug("Bluesky username %s, password %s, client %s", BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)
                    logger.info("Set up bluesky service")

                    post = posts['short']

        logger.info('Done getting services for %s.', bot['name'])                                                           

        
                                                    
        # for found_services in bot['bots]']:
        #     logger.debug("Found service %s: ", found_services)
        # logger.debug(bot)


    # get our tracery rules
    rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

    # generate our posts dict containing a short post and a long post
    post = generate_posts(rules)

    # send that post to um a posting thing
    # logger.info('Posting to Mastodon')
    # post_to_mastodon(post)
    # logger.info('Posting to Bluesky')
    # post_to_bluesky(post)

    logger.info('Finished')

if __name__ == '__main__':
    main()

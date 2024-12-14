import os
import logging
import json
import pyjson5
from dotenv import load_dotenv
import argparse

# Bot utilities
from utils.tracery import get_rules, generate_posts, generate_bluesky_thread
from utils.mastodon import get_mastodon_client
from utils.bluesky import get_bluesky_instance, bluesky_faceted_post, post_thread

import pprint

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

# make a mastodon client and then post
def post_to_mastodon(post):
    mastodon_instance = mastodon_client()
    mastodon_instance.status_post(post["long"])

# make a bluesky client 
def post_to_bluesky(post):
    bluesky_client = bluesky_instance()
    bluesky_post = bluesky_faceted_post(post["short"])
    bluesky_client.post(bluesky_post)

service_handlers = {
    'bluesky': post_to_bluesky,
    'mastodon': post_to_mastodon,
}

CONST_BOTFILE_DEFAULT = 'bots.json'


def main():

    logger.info('***** Started')

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='bots.json')
    parser.add_argument('-b', '--botfile')
    parser.add_argument('-o', '--off', action="store_true")
    args = parser.parse_args()

    argument_botfile = args.botfile

    # parser.add_argument("-o", "--only", choices=['bluesky','mastodon'])
    # if args.only:
    #     logger.info("Found an only argument, %s", args.only)

    # else:
    #     logger.info("No only argument")

    # Set a botfile if one was provided

    logger.debug('args: %s', parser.parse_args())
    BOTFILE = ''

    if args.filename or args.botfile:
        if args.filename:
            logger.info('Found a filename argument, %s', args.filename)
            BOTFILE = args.filename

        if args.botfile:
            logger.info('Found a botfile argument, %s', args.botfile)
            BOTFILE = args.botfile 
        
    else:
        BOTFILE = CONST_BOTFILE_DEFAULT


    NO_POST = False

    if args.off:
        NO_POST = True

    # Set the grammars directory from os environment
    GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
    logger.info('Using grammars directory from env: %s"', GRAMMARS_DIRECTORY)
    
    # get the bots
    logger.info('Opening this json file %s', BOTFILE)
    
    with open(BOTFILE) as bots_json:
        bots = pyjson5.decode_io(bots_json)
    
    logger.info("Found %s bots", len(bots))

    for idx, bot in enumerate(bots):
        logger.info('##### Starting bot %s of %s: %s', idx+1, len(bots), bot['name'])

        # Get the grammars
        GRAMMAR_JSON = bot['grammar_json']
        logger.debug("Bot '%s' using grammar %s", bot['name'], bot['grammar_json'])

        logger.info('Getting rules for %s...', bot['name'])
        rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

        # Now we're doing corpora stuff
        if 'corpora' in bot:

            corpora_files = bot['corpora']
            logger.info('Found corpora %s', corpora_files)
            for corpus in corpora_files:
                rules.update(get_rules('grammars/corpora',corpus))
    
        # Generate a post
        logger.info('Starting post generation for %s...', bot['name'])
        posts = generate_posts(rules)
        logger.info('Generated a posts object %s', posts)
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

                    
                    if NO_POST:
                        logger.info("NO_POST is %s so we're not posting for Mastodon",NO_POST)

                    if not NO_POST:
                        post = posts['long']
                        mastodon_instance = get_mastodon_client(MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                        mastodon_instance.status_post(post)
                        logger.info('Posted to Mastodon: %s', post)


                case 'bluesky':
                    logger.info("Found a bluesky service")
                    BLUESKY_USERNAME = service['username']
                    BLUESKY_PASSWORD = service['password']
                    BLUESKY_CLIENT = service['client']
                    logger.debug("Bluesky username %s, password %s, client %s", BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)
                    logger.info("Set up bluesky service")


                    isThreaded = False

                    if 'threaded' in service:
                        isThreaded = service['threaded']

                    logger.info("Threaded? %s", isThreaded)

                    if NO_POST:
                        logger.info("NO_POST is %s so we're not posting for Bluesky",NO_POST)

                    if not NO_POST:
                        bluesky_client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)

                        if isThreaded:
                            thread_of_posts = generate_bluesky_thread(rules)
                            post_thread(thread_of_posts, bluesky_client)

                        else:
                            post = posts['short']
                            bluesky_post = bluesky_faceted_post(post)
                            bluesky_client.post(bluesky_post)
                        logger.info('Posted to Bluesky: %s', post)

        logger.info('Done getting services for %s.', bot['name'])                                                           


    logger.info('Finished')

if __name__ == '__main__':
    main()

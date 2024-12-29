import os
import sys
import logging
import json
import pyjson5
from dotenv import load_dotenv
import argparse

# Bot utilities
from utils.tracery import get_rules, generate_posts, generate_bluesky_thread
from utils.mastodon import get_mastodon_client
from utils.bluesky import get_bluesky_instance, bluesky_faceted_post, post_thread

# use this to valiate that bots.json has at least some stuff in it
from jsonschema import validate

# Define the schema for bots.json
# I should move this somewhere else
BOT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of your bot"
        },
        "grammar_json": {
            "type": "string",
            "description": "Name of the Tracery grammar file"
        },
        "directory": {
            "type": "string",
            "description": "Directory path to the grammar files"
        },
        "corpora": {
            "type": "array",
            "description": "List of corpora file names",
            "items": {
                "type": "string"
            }
        },
        "service": {
            "type": "array",
            "description": "List of services the bot connects to",
            "items": {
                "type": "object",
                "properties": {
                    "test_username": {
                        "type": "string",
                        "description": "Test user name"
                    },
                    "test_password": {
                        "type": "string",
                        "description": "Test user password"
                    },
                    "service_type": {
                        "type": "string",
                        "description": "Type of service (e.g., 'bluesky')"
                    },
                    "username": {
                        "type": "string",
                        "description": "Service username"
                    },
                    "password": {
                        "type": "string",
                        "description": "Service password"
                    },
                    "client": {
                        "type": "string",
                        "description": "Client URL for the service"
                    },
                    "threaded": {
                        "type": "boolean",
                        "description": "Whether threading is enabled"
                    },
                    "service_token": {
                        "type": "string",
                        "description": "Your Mastodon access token"
                    },
                    "base_url": {
                        "type": "string",
                        "description": "Your Mastodon instance base URL"
                    }
                },
                "if": {
                    "properties": {
                        "service_type": {"const": "mastodon"}
                    },
                    "required": ["access_token", "base_url"]
                },
            "then": { "required": ["service_type", "threaded"] }

            },
        },
    },
    "required": ["name", "grammar_json", "directory", "service"]
}

DEFAULT_GRAMMAR_DIR = 'grammars/'


import pprint

# set up the logger
logger = logging.getLogger('bot-bot-bot')
logger.setLevel(logging.DEBUG)

# Console logging handler set to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File logging handler set to info
fh = logging.FileHandler('bot-bot-bot.log')
fh.setLevel(logging.DEBUG)

# Set the formatter for root
ch_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S')
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s: %(funcName)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(ch_formatter)
fh.setFormatter(fh_formatter)

# add console and file handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

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
BOTFILE = ''

def main():

    logger.debug('***** Started ******')

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='bots.json', help="Supply a json file defining your bots, otherwise bots.json")
    parser.add_argument('-b', '--botfile', help="Supply a json file defining your bots")
    parser.add_argument('-o', '--off', action="store_true", help="Do not post to any networks")
    parser.add_argument('-t', '--test', action="store_true", help="Use test credentials supplied in bot json")
    args = parser.parse_args()

    argument_botfile = args.botfile

    logger.debug('args: %s', parser.parse_args())

    if args.filename or args.botfile:
        if args.filename:
            logger.debug('Found a filename argument, %s', args.filename)
            BOTFILE = args.filename

        if args.botfile:
            logger.debug('Found a botfile argument, %s', args.botfile)
            BOTFILE = args.botfile 
        
    else:
        BOTFILE = CONST_BOTFILE_DEFAULT


    NO_POST = False
    USE_TEST = False

    if args.off:
        NO_POST = True
        logger.info("Running with option --off, so will generate posts but not post.")

    if args.test:
        USE_TEST = True
        logger.info("Running with option --test, so will use test credentials.")
    
    logger.debug("Test flag %s", USE_TEST)


    # get the bots from the bot json
    
    try: 

        with open(BOTFILE) as bots_json:
            logger.debug('Opening this json file %s', BOTFILE)
            bots = pyjson5.decode_io(bots_json)
            
    except IOError:
        logger.info("Couldn't open botfile %s, are you sure it exists?", BOTFILE)
        sys.exit()

    botnames = ", ".join(bot['name'] for bot in bots)

    logger.info("Found %s bots: %s", len(bots), botnames)

    for idx, bot in enumerate(bots):
        NO_POST = args.off

        # pulled the bot object out, so let's validate
        validate(instance=bot, schema=BOT_SCHEMA)

        logger.info('##### Starting bot %s of %s: %s', idx+1, len(bots), bot['name'])

        # Get the grammars
        GRAMMAR_JSON = bot['grammar_json']
        logger.debug("Bot '%s' using grammar %s", bot['name'], bot['grammar_json'])

        # if there's an overriden grammars location:
        GRAMMARS_DIRECTORY = DEFAULT_GRAMMAR_DIR if not bot.get('directory') else bot.get('directory')

        logger.debug('Getting rules for %s...', bot['name'])
        rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)
        logger.info('%s: Loaded rules.', bot['name'])

        # Now we're doing corpora stuff
        if 'corpora' in bot:
            corpora_files = bot['corpora']
            logger.debug('Found corpora %s for %s.', corpora_files, bot['name'])
            for corpus in corpora_files:
                rules.update(get_rules(GRAMMARS_DIRECTORY, corpus))
            logger.info("%s: Loaded %s additional corpora.", bot['name'], len(bot['corpora']), )

    
        # Generate a post
        posts = generate_posts(rules)
        logger.info('Generated a posts object %s', posts)

        # Getting services

        bot_services = ", ".join(service['service_type'] for service in bot['service'])

        logger.debug('Getting services for %s, found:', bot['name'])
        for idx, service in enumerate(bot['service']):

            logger.debug("Service %s of %s for %s: %s", idx+1, len(bot['service']), bot['name'], service['service_type'])
        
            match service['service_type']:
                
                case 'mastodon':
                    logger.debug("Found a mastodon service")
                    MASTODON_ACCESS_TOKEN = service['access_token']
                    MASTODON_BASE_URL = service['base_url']
                    logger.debug("Mastodon token %s, base URL %s", MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                    logger.info("Set up mastodon service for %s", bot['name'])

                    
                    if NO_POST:
                        logger.info("Not posting because -off is %s", NO_POST)

                    if not NO_POST:
                        post = posts['long']
                        mastodon_instance = get_mastodon_client(MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                        mastodon_instance.status_post(post)
                        logger.info('Posted to Mastodon: %s', post)


                case 'bluesky':
                    if USE_TEST:
                        try:
                            BLUESKY_USERNAME=service['test_username']
                            BLUESKY_PASSWORD=service['test_password']
                            logger.info("Using the test account %s", service['test_username'])

                        except Exception as error:
                            logger.debug("%s was raised",type(error).__name__)
                            logger.info("Couldn't find test account, so will set NO_POST to True.")
                            logger.info("NO_POST was: %s", NO_POST)
                            NO_POST = True
                            logger.info("NO_POST should be True now %s", NO_POST)
                                        
                            break
                    else:
                        BLUESKY_USERNAME = service['username']
                        BLUESKY_PASSWORD = service['password']

                    BLUESKY_CLIENT = service['client']
                    logger.debug("Bluesky username %s, password %s, client %s", BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)
                    logger.info("%s: Set up Bluesky service for %s", bot['name'], BLUESKY_USERNAME)


                    isThreaded = False

                    if 'threaded' in service:
                        isThreaded = service['threaded']

                    logger.debug("Threaded? %s", isThreaded)

                    if NO_POST:
                        logger.info("NO_POST is %s so we're not posting for Bluesky", NO_POST)

                    if not NO_POST:
                        bluesky_client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)

                        if isThreaded:
                            thread_of_posts = generate_bluesky_thread(rules)
                            post_thread(thread_of_posts, bluesky_client)
                            logger.info('Posted to Bluesky: %s', post_thread)


                        else:
                            post = posts['short']
                            bluesky_post = bluesky_faceted_post(post)
                            bluesky_client.post(bluesky_post)
                            logger.info('Posted to Bluesky: %s', post)

        
                
    logger.debug('Finished')

if __name__ == '__main__':
    main()

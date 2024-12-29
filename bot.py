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
ch_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
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


def main():

    logger.info('***** Started ******')

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='bots.json', help="Supply a json file defining your bots, otherwise bots.json")
    parser.add_argument('-b', '--botfile', help="Supply a json file defining your bots")
    parser.add_argument('-o', '--off', action="store_true", help="Do not post to any networks")
    parser.add_argument('-t', '--test', action="store_true", help="Use test credentials supplied in bot json")
    args = parser.parse_args()

    argument_botfile = args.botfile

    logger.debug('args: %s', parser.parse_args())
    BOTFILE = ''

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

    if args.test:
        USE_TEST = True
    
    logger.debug("Test flag %s", USE_TEST)

    # Set the grammars directory from os environment
    # GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
    # logger.info('Using grammars directory from env: %s"', GRAMMARS_DIRECTORY)
    
    # get the bots
    
    try: 

        with open(BOTFILE) as bots_json:
            logger.info('Opening this json file %s', BOTFILE)
            bots = pyjson5.decode_io(bots_json)
            
    except IOError:
        logger.info("Couldn't open botfile %s, are you sure it exists?", BOTFILE)
        sys.exit()
    
    logger.info("Found %s bots", len(bots))

    for idx, bot in enumerate(bots):

        # pulled the bot object out, so let's validate
        validate(instance=bot, schema=BOT_SCHEMA)

        logger.info('##### Starting bot %s of %s: %s', idx+1, len(bots), bot['name'])

        # Get the grammars
        GRAMMAR_JSON = bot['grammar_json']
        logger.debug("Bot '%s' using grammar %s", bot['name'], bot['grammar_json'])

        # if there's an overriden grammars location:

        GRAMMARS_DIRECTORY = DEFAULT_GRAMMAR_DIR if not bot.get('directory') else bot.get('directory')

        logger.debug("env is %s, override is %s", os.getenv("GRAMMARS_DIRECTORY"), bot.get('directory') )

        # logger.debug('what did we do? %s', SET_FROM_JSON_OTHERWISE_OS_ENV)

        # logger.debug("bot grammar directory key is populated %s", )
        # GRAMMARS_DIRECTORY = bot['grammar_directory'] if not bot['grammar_directory'] else GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")


        logger.info('Getting rules for %s...', bot['name'])
        rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

        # Now we're doing corpora stuff
        if 'corpora' in bot:

            corpora_files = bot['corpora']
            logger.info('Found corpora %s', corpora_files)
            for corpus in corpora_files:
                rules.update(get_rules(GRAMMARS_DIRECTORY, corpus))
    
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

                    if USE_TEST:
                        try:
                            logger.info("Using the test account")
                            BLUESKY_USERNAME=service['test_username']
                            BLUESKY_PASSWORD=service['test_password']
                        except Exception as error:
                            logger.debug("%s was raised",type(error).__name__)
                            sys.exit()
                    else:
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

import os
import pprint
import json
from dotenv import load_dotenv
from utils.tracery import get_rules, generate_posts
from utils.mastodon import mastodon_client_multiple
from utils.bluesky import bluesky_instance, bluesky_instance_multiple, bluesky_faceted_post

# Let's define some bots: 

bots = []

bot_starfleet_jobs = {
    'name' : 'Starfleet Jobs',
    'grammar_json' : 'starfleetjobs.json',
    'services' : [{
            'type': 'mastodon',
            'access_token' : 'mP_PoDHqE0buKi6yND9xh0qBzPkN8v0AeJZQY9Rv9uY',
            'base_url' : 'https://botsin.space/',
            },
            {
            'type' : 'bluesky',
            'username' : 'starfleetjobs.bsky.social',
            'password' : '7ic4-lho6-inut-lwrs',
            'client' : 'https://bsky.social'
            }
            ]
}

bot_breaking_govtech = {
    'name' : 'Breaking Govtech',
    'grammar_json' : 'breaking_govtech.json',
    'services' : [{
            'type': 'mastodon',
            'access_token' : 'WpsYVKjlneM9dCtqX69QnIshXIHd_HqWUFamPWFMk4c',
            'base_url' : 'https://botsin.space/',
            'grammar_json' : 'breaking_govtech.json'
            }
            ]
}

bots = [bot_starfleet_jobs, bot_breaking_govtech]

# Load and set environment variables
load_dotenv()

# let's run the bots!
for bot in bots:
    
    # set grammars for this bot
    
    GRAMMARS_DIRECTORY = os.getenv("GRAMMARS_DIRECTORY")
    GRAMMAR_JSON = bot['grammar_json']

    # get the rules for this bot...
    rules = get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON)

    # ... and then generate a post (long and short) based on those rules
    posts = generate_posts(rules)


    # now figure out what services to post to, and how
    # how many services does this bot have?
    for service in bot['services']:
        pprint.pp(service)

        match service['type']:
            case 'mastodon':
                print("mastodon! so we should use this access token: " + service['access_token'])

                MASTODON_ACCESS_TOKEN = service['access_token']
                MASTODON_BASE_URL = service['base_url']

                post = posts['long']

                mastodon_instance = mastodon_client_multiple(MASTODON_ACCESS_TOKEN, MASTODON_BASE_URL)
                mastodon_instance.status_post(post)
                print("Posted to Mastodon: " + post)

                
            case 'bluesky':
                print("bluesky! so we should use this username: " + service['username'])
                BLUESKY_USERNAME = service['username']
                BLUESKY_PASSWORD = service['password']
                BLUESKY_CLIENT = service['client']

                post = posts['short']

                bluesky_client = bluesky_instance_multiple(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)
                bluesky_post = bluesky_faceted_post(post)
                bluesky_client.post(bluesky_post)
                print("Posted to Bluesky: " + post)

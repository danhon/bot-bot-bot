import os
from dotenv import load_dotenv
import logging
import pprint
import json
import re

from mastodon import Mastodon

# create logger
module_logger = logging.getLogger('bot-bot-bot.utils.mastodon')

def mastodon_client():
    """Returns a usable Mastodon instance based on the environment variables MASTODON_TOKEN and MASTODON_BASE_URL"""
    environment = envs()
    MASTODON_TOKEN = environment["MASTODON_TOKEN"]
    MASTODON_BASE_URL = environment["MASTODON_BASE_URL"]

    module_logger.debug('Using token %s', MASTODON_TOKEN)
    module_logger.debug('Using base URL %s', MASTODON_BASE_URL)

    mastodon_instance = Mastodon(
        access_token=MASTODON_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    return mastodon_instance


def get_mastodon_client(token, base_url):
    MASTODON_TOKEN = token
    MASTODON_BASE_URL = base_url

    mastodon_instance = Mastodon(
        access_token=MASTODON_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    return mastodon_instance

def envs():
    load_dotenv()
    return os.environ
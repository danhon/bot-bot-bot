import logging
from mastodon import Mastodon

# create logger
module_logger = logging.getLogger('bot-bot-bot.utils.mastodon')

def get_mastodon_client(token, base_url):
    MASTODON_TOKEN = token
    MASTODON_BASE_URL = base_url

    mastodon_instance = Mastodon(
        access_token=MASTODON_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    return mastodon_instance

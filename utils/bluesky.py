import re
import logging

from atproto import Client, client_utils

# create logger
module_logger = logging.getLogger('bot-bot-bot.utils.bluesky')

def get_bluesky_instance(username, password, client_url):
    """Returns a Bluesky client based on provided username, password, and url"""
    
    module_logger.debug('Using %s, %s, %s for username, password, client', username, password, client_url)
    client = Client(client_url)
    client.login(username, password)
    
    return client

def bluesky_faceted_post(post):
    """Returns a textbuilder object with tags"""
    post_without_tags = post.split('#')[0]

    text_builder = client_utils.TextBuilder()
    text_builder.text(post_without_tags)

    # parse the hashtags
    hashtags = re.findall(r"#\w+", post)
    # pprint.pp(hashtags)
 
    # add tags 
    for tag in hashtags:
        # Add each hashtag as a tag facet
        text_builder.tag(tag + " ", tag.split('#')[1])

    return text_builder


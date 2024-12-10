import re
import logging
import json

from atproto import Client, client_utils
from atproto import models

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
    text_builder = client_utils.TextBuilder()
    
    parts = re.split(r'(#\w+)', post)

    post_list = [part for part in parts if part]

    for fragment in post_list:
        if re.match(r'#\w+', fragment):
            text_builder.tag(fragment, fragment.split('#')[1])
        else:
            text_builder.text(fragment)


    # post_without_tags = post.split('#')[0]
    # text_builder.text(post_without_tags)

    # text_builder.text(post)

    # parse the hashtags
    # hashtags = re.findall(r"#\w+", post)
    # pprint.pp(hashtags)
 
    # add tags 
    # for tag in hashtags:
    #     # Add each hashtag as a tag facet
    #     text_builder.tag(tag + " ", tag.split('#')[1])

    return text_builder


def bluesky_reply(parent_post, root_post, post, client):

    parent = models.create_strong_ref(parent_post)
    root = models.create_strong_ref(root_post)

    this_post = client.send_post(
        text = post,
        reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
    )   
    return this_post

class BlueskyThreadPost:
    text = None
    post = None
    post_root = None
    post_parent = None


    def __init__(self):

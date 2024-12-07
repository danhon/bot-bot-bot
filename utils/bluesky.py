import os
from dotenv import load_dotenv
import pprint
import json
import re

from atproto import Client, client_utils

def bluesky_instance():
    """Returns a Bluesky client based on the environment variables BLUESKY_USERNAME and BLUESKY_PASSWORD. Assumes that your client/pds is at bsky.social"""
    environment = envs()
    BLUESKY_USERNAME = environment["BLUESKY_USERNAME"]
    BLUESKY_PASSWORD = environment["BLUESKY_PASSWORD"]

    client = Client("https://bsky.social")

    client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
    # print("generated a client")
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

def envs():
    load_dotenv()
    return os.environ
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

    return text_builder


def bluesky_reply(parent_post, root_post, post, client):

    parent = models.create_strong_ref(parent_post)
    root = models.create_strong_ref(root_post)

    this_post = client.send_post(
        text = post,
        reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
    )   
    return this_post

def post_thread(thread_of_posts, client):

    for idx, post in enumerate(thread_of_posts):
        print(idx, len(post.text), post.text)

        
        if idx == 0:
            this_post = client.send_post(post.facetedpost)
            root_post = this_post

            post.root_post = root_post
            post.post = this_post

        
        else: 
            previous_post = thread_of_posts[idx-1]

            root_post = previous_post.root_post
            # print(root_post)
            parent_post = previous_post.post

            parent = models.create_strong_ref(parent_post)
            root = models.create_strong_ref(root_post)
                    
            this_post = client.send_post(
                text = post.facetedpost,
                reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
            )

            post.root_post = root_post
            post.parent_post = parent_post
            post.post = this_post
            print (idx, post.parent_post)


class Post_in_Thread:
    text = None
    facetedpost = None
    post = None
    parent_post = None
    root_post = None

    def __init__(self, text, facetedpost, post=None, parent_post=None, root_post=None):
        self.text = text
        self.facetedpost = facetedpost
        self.post = post
        self.parent_post = parent_post
        self.root_post = root_post
        